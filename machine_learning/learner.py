from datetime import datetime
import tensorflow
import tensorflow_transform as tft
import tensorflow.contrib.eager as tfe
import tensorflow_transform.beam as tft_beam
from data_fetcher import DataFetcher
from numpy import array
from tensorflow_transform.tf_metadata import dataset_metadata
from tensorflow_transform.tf_metadata import dataset_schema
from sklearn.model_selection import KFold

tensorflow.enable_eager_execution()


def preprocess(data):
    early_slack_count_normalized = tft.scale_to_0_1(data["early_slack_count"])
    midday_slack_count_normalized = tft.scale_to_0_1(data["midday_slack_count"])
    late_slack_count_normalized = tft.scale_to_0_1(data["late_slack_count"])
    negative_emoji_normalized = tft.scale_to_0_1(data["negative_emoji"])
    neutral_emoji_normalized = tft.scale_to_0_1(data["neutral_emoji"])
    positive_emoji_normalized = tft.scale_to_0_1(data["positive_emoji"])
    github_count_normalized = tft.scale_to_0_1(data["github_count"])
    event_rating_normalized = tft.scale_to_0_1(data["event_rating_ratio"])
    temperature_normalized = tft.scale_to_0_1(data["temperature"])
    precipitation_normalized = tft.scale_to_0_1(data["precipitation"])

    out = {
        "early_slack_count_normalized": early_slack_count_normalized,
        "midday_slack_count_normalized": midday_slack_count_normalized,
        "late_slack_count_normalized": late_slack_count_normalized,
        "negative_emoji_normalized": negative_emoji_normalized,
        "neutral_emoji_normalized": neutral_emoji_normalized,
        "positive_emoji_normalized": positive_emoji_normalized,
        "github_count_normalized": github_count_normalized,
        "weekday": data["weekday"],
        "event_rating_normalized": event_rating_normalized,
        "temperature_normalized": temperature_normalized,
        "precipitation_normalized": precipitation_normalized

    }
    return out


def baseline_model():
    model = tensorflow.keras.Sequential()
    # TODO: Once you have more data figure out which is the best model. LSTM or just dense.
    model.add(tensorflow.keras.layers.Embedding(20, output_dim=1000))
    model.add(tensorflow.keras.layers.LSTM(100))
    # model.add(tensorflow.keras.layers.Dense(1000, input_dim=8))
    # model.add(tensorflow.keras.layers.Dense(100))
    # model.add(tensorflow.keras.layers.Dense(10))
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
                # early_slack_count, midday_slack_count and late_slack_count is when a
                # slack message was sent in the day.
                'early_slack_count': tensorflow.FixedLenFeature([], tensorflow.int64),
                'midday_slack_count': tensorflow.FixedLenFeature([], tensorflow.int64),
                'late_slack_count': tensorflow.FixedLenFeature([], tensorflow.int64),
                # negative_emoji, positive_emoji and neutral_emoji is the sentiment
                # of the emojis sent.
                'negative_emoji': tensorflow.FixedLenFeature([], tensorflow.int64),
                'positive_emoji': tensorflow.FixedLenFeature([], tensorflow.int64),
                'neutral_emoji': tensorflow.FixedLenFeature([], tensorflow.int64),
                # Github count
                'github_count': tensorflow.FixedLenFeature([], tensorflow.int64),
                # weekday
                'weekday': tensorflow.FixedLenFeature([], tensorflow.int64),
                'event_rating_ratio': tensorflow.FixedLenFeature([], tensorflow.int64),
                'temperature': tensorflow.FixedLenFeature([], tensorflow.int64),
                'precipitation': tensorflow.FixedLenFeature([], tensorflow.int64),
            }))

        transformed_dataset, transform_fn = (
                (data, raw_data_metadata) | tft_beam.AnalyzeAndTransformDataset(preprocess))
        transformed_data, transformed_metadata = transformed_dataset

    # TODO: There should be an easier way to do this.
    retransformed_data = []
    for trans in transformed_data:
        current = [trans["early_slack_count_normalized"],
                   trans["midday_slack_count_normalized"],
                   trans["late_slack_count_normalized"],
                   trans["negative_emoji_normalized"],
                   trans["neutral_emoji_normalized"],
                   trans["positive_emoji_normalized"],
                   trans["github_count_normalized"],
                   trans["weekday"],
                   trans["event_rating_normalized"],
                   trans["temperature_normalized"],
                   trans["precipitation_normalized"]]

        retransformed_data.append(current)

    return array(retransformed_data)


def make_dataset(X_data, y_data, n_splits):
    """
    :param X_data: All the x_data as a numpy array
    :param y_data: All the y_data as a numpy array
    :param n_splits: How many splits
    :return: Performs k-fold cross validation and returns a generator for x_data, y_data,
    x_train and y_train.
    """

    def gen():
        for train_index, test_index in KFold(n_splits).split(X_data):
            X_train, X_test = X_data[train_index], X_data[test_index]
            y_train, y_test = y_data[train_index], y_data[test_index]
            yield X_train, y_train, X_test, y_test

    return tensorflow.data.Dataset.from_generator(gen, (
        tensorflow.float64, tensorflow.float64, tensorflow.float64, tensorflow.float64))


def train(date=None, days=1):
    if date is None:
        date = datetime.now()

    raw_x_data, y_data = DataFetcher.fetch_data(date, days=days)

    print(raw_x_data)
    print(y_data)

    raw_x_data = array(raw_x_data)
    y_data = array(y_data)

    x_data = transform_data(raw_x_data)
    print(x_data)
    model = baseline_model()

    n_splits = 5
    dataset = make_dataset(x_data, y_data, n_splits)
    for X_train, y_train, X_test, y_test in tfe.Iterator(dataset):
        model.fit(X_train, y_train, epochs=1000)
        model.evaluate(X_test, y_test)
    return model


def predict(model, data):
    return model.predict(data)


def main():
    start_date = datetime(2019, 7, 23, 22, 23, 29)
    model = train(start_date, days=365)

    raw_data = [
        {'weekday': 2, 'early_slack_count': 113, 'midday_slack_count': 56, 'late_slack_count': 87,
         'negative_emoji': 0, 'positive_emoji': 0, 'neutral_emoji': 0, 'github_count': 6,
         'event_rating_ratio': 0, 'temperature': 0, 'precipitation': 0},
        {'weekday': 3, 'early_slack_count': 22, 'midday_slack_count': 38, 'late_slack_count': 23,
         'negative_emoji': 0, 'positive_emoji': 0, 'neutral_emoji': 0, 'github_count': 10,
         'event_rating_ratio': 0, 'temperature': 0, 'precipitation': 0},
        {'weekday': 4, 'early_slack_count': 67, 'midday_slack_count': 83, 'late_slack_count': 23,
         'negative_emoji': 0, 'positive_emoji': 0, 'neutral_emoji': 0, 'github_count': 12,
         'event_rating_ratio': 0, 'temperature': 0, 'precipitation': 0},
        {'weekday': 0, 'early_slack_count': 12, 'midday_slack_count': 107, 'late_slack_count': 78,
         'negative_emoji': 1, 'positive_emoji': 15, 'neutral_emoji': 2, 'github_count': 11,
         'event_rating_ratio': 0, 'temperature': 0, 'precipitation': 0},
        {'weekday': 1, 'early_slack_count': 55, 'midday_slack_count': 117, 'late_slack_count': 111,
         'negative_emoji': 0, 'positive_emoji': 29, 'neutral_emoji': 3, 'github_count': 15,
         'event_rating_ratio': 0, 'temperature': 0, 'precipitation': 0},
        {'weekday': 2, 'early_slack_count': 78, 'midday_slack_count': 126, 'late_slack_count': 117,
         'negative_emoji': 2, 'positive_emoji': 140, 'neutral_emoji': 6, 'github_count': 7,
         'event_rating_ratio': 0, 'temperature': 164, 'precipitation': 0},
        {'weekday': 3, 'early_slack_count': 42, 'midday_slack_count': 218, 'late_slack_count': 130,
         'negative_emoji': 3, 'positive_emoji': 40, 'neutral_emoji': 4, 'github_count': 5,
         'event_rating_ratio': 0, 'temperature': 201, 'precipitation': 0}]
    data = transform_data(raw_data)

    prediction = predict(model, data)

    # Should print: 0.83333333, 1.0, 0.8, 0.8, 0.96153846, 0.73333333, 0.96153846
    print(prediction)


if __name__ == '__main__':
    main()
