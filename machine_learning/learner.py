from datetime import datetime
import tensorflow
import tensorflow_transform as tft
import tensorflow_transform.beam as tft_beam
from data_fetcher import DataFetcher
from numpy import array
from tensorflow_transform.tf_metadata import dataset_metadata
from tensorflow_transform.tf_metadata import dataset_schema


def preprocess(data):
    earlies_normalized = tft.scale_to_0_1(data["earlies"])
    middays_normalized = tft.scale_to_0_1(data["middays"])
    lates_normalized = tft.scale_to_0_1(data["lates"])
    negative_normalized = tft.scale_to_0_1(data["negative"])
    neutral_normalized = tft.scale_to_0_1(data["neutral"])
    positive_normalized = tft.scale_to_0_1(data["positive"])
    github_count_normalized = tft.scale_to_0_1(data["github_count"])

    out = {
        "earlies_normalized": earlies_normalized,
        "middays_normalized": middays_normalized,
        "lates_normalized": lates_normalized,
        "negative_normalized": negative_normalized,
        "neutral_normalized": neutral_normalized,
        "positive_normalized": positive_normalized,
        "github_count_normalized": github_count_normalized

    }
    return out


def baseline_model():
    model = tensorflow.keras.Sequential()
    # TODO: Once you have more data figure out which is the best model. LSTM or just dense.
    # model.add(tensorflow.keras.layers.Embedding(6, output_dim=1000))
    # model.add(tensorflow.keras.layers.LSTM(100))
    model.add(tensorflow.keras.layers.Dense(1000, input_dim=7))
    model.add(tensorflow.keras.layers.Dense(100))
    model.add(tensorflow.keras.layers.Dense(10))
    model.add(tensorflow.keras.layers.Dense(1, activation='sigmoid'))
    model.compile(
        optimizer="adam",
        loss="mean_absolute_error",  # It seems that for now mean_absolute_error is better than
        # squared_error.
        metrics=['mean_absolute_error', 'mean_squared_error'])

    return model


def transform_data(data):
    """
    :param data: A list of raw data.
    :return: A numpy array of arrays of integers.
    """
    with tft_beam.Context(temp_dir="temp/"):
        raw_data_metadata = dataset_metadata.DatasetMetadata(
            dataset_schema.from_feature_spec({
                # earlies, middays and lates is when a slack message was sent in the day.
                'earlies': tensorflow.FixedLenFeature([], tensorflow.int64),
                'middays': tensorflow.FixedLenFeature([], tensorflow.int64),
                'lates': tensorflow.FixedLenFeature([], tensorflow.int64),
                # negative, positive and neutral is the sentiment of the emojis sent.
                'negative': tensorflow.FixedLenFeature([], tensorflow.int64),
                'positive': tensorflow.FixedLenFeature([], tensorflow.int64),
                'neutral': tensorflow.FixedLenFeature([], tensorflow.int64),
                # Github count
                'github_count': tensorflow.FixedLenFeature([], tensorflow.int64),

            }))

        transformed_dataset, transform_fn = (
                (data, raw_data_metadata) | tft_beam.AnalyzeAndTransformDataset(preprocess))
        transformed_data, transformed_metadata = transformed_dataset

    # TODO: There should be an easier way to do this.
    retransformed_data = []
    for trans in transformed_data:
        current = [trans["earlies_normalized"],
                   trans["middays_normalized"],
                   trans["lates_normalized"],
                   trans["negative_normalized"],
                   trans["neutral_normalized"],
                   trans["positive_normalized"],
                   trans["github_count_normalized"]]

        retransformed_data.append(current)

    return array(retransformed_data)


def train(date=None, days=1):
    if date is None:
        date = datetime.now()

    raw_x_data, y_data = DataFetcher.fetch_data(date, days=days)

    print(raw_x_data)
    print(y_data)

    transformed_data = transform_data(raw_x_data)
    print(transformed_data)
    model = baseline_model()
    model.fit(transformed_data, y_data, epochs=1000)
    return model


def predict(model, data):
    return model.predict(data)


def main():
    # TODO: move all of this to amazon sagemaker

    start_date = datetime(2019, 7, 23, 22, 23, 29)
    model = train(start_date, days=10)

    raw_data = [
        {'earlies': 113, 'middays': 56, 'lates': 87, 'negative': 0, 'positive': 0, 'neutral': 0,
         'github_count': 6},
        {'earlies': 22, 'middays': 38, 'lates': 23, 'negative': 0, 'positive': 0, 'neutral': 0,
         'github_count': 10},
        {'earlies': 67, 'middays': 83, 'lates': 23, 'negative': 0, 'positive': 0, 'neutral': 0,
         'github_count': 12},
        {'earlies': 12, 'middays': 107, 'lates': 33, 'negative': 1, 'positive': 12, 'neutral': 2,
         'github_count': 2}]
    data = transform_data(raw_data)

    prediction = predict(model, data)
    print(prediction)  # Should print: [0.83333333, 1.0, 0.8, 1.0]
    # res = [0.83333333, 1.0, 0.8]
    # acc = model.evaluate(data, res)


if __name__ == '__main__':
    main()
