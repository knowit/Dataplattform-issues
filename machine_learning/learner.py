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

    out = {
        "earlies_normalized": earlies_normalized,
        "middays_normalized": middays_normalized,
        "lates_normalized": lates_normalized
    }
    return out


def process_slack_data(data):
    earlies = 0
    middays = 0
    lates = 0
    for slack_data in data["SlackType"]:
        time_of_day = slack_data["time_of_day"]
        if time_of_day == "early":
            earlies += 1
        elif time_of_day == "midday":
            middays += 1
        elif time_of_day == "late":
            lates += 1
    del data["SlackType"]
    data["earlies"] = earlies
    data["middays"] = middays
    data["lates"] = lates
    return data


def baseline_model():
    model = tensorflow.keras.Sequential()
    model.add(tensorflow.keras.layers.Dense(1000, input_dim=3))
    model.add(tensorflow.keras.layers.Dense(100))
    model.add(tensorflow.keras.layers.Dense(10))
    model.add(tensorflow.keras.layers.Dense(1, activation='sigmoid'))
    model.compile(
        optimizer="adam",
        loss="mean_squared_error",
        metrics=['accuracy'])

    return model


def transform_data(data):
    """
    :param data: A list of raw data.
    :return: A numpy array of arrays of integers.
    """
    with tft_beam.Context(temp_dir="temp/"):
        raw_data_metadata = dataset_metadata.DatasetMetadata(
            dataset_schema.from_feature_spec({
                'earlies': tensorflow.FixedLenFeature([], tensorflow.int64),
                'middays': tensorflow.FixedLenFeature([], tensorflow.int64),
                'lates': tensorflow.FixedLenFeature([], tensorflow.int64),
            }))

        transformed_dataset, transform_fn = (
                (data, raw_data_metadata) | tft_beam.AnalyzeAndTransformDataset(preprocess))
        transformed_data, transformed_metadata = transformed_dataset

    # TODO: There should be an easier way to do this.
    retransformed_data = []
    for trans in transformed_data:
        current = [trans["earlies_normalized"],
                   trans["middays_normalized"],
                   trans["lates_normalized"]]
        retransformed_data.append(current)
    return array(retransformed_data)


def train(date=None, days=1):
    if date is None:
        date = datetime.now()

    raw_x_data, y_data = DataFetcher.fetch_data(date, days=days)

    x_data = list(map(process_slack_data, raw_x_data))
    print(x_data)
    print(y_data)

    # # TODO: Remove hardcoded test-data.
    # x_data = [{'earlies': 10, 'middays': 20, 'lates': 25},
    #           {'earlies': 50, 'middays': 70, 'lates': 49},
    #           {'earlies': 112, 'middays': 99, 'lates': 109}]
    # y_data = [0.2, 0.6, 0.9]
    # # TODO: End of hardcoded test-data.
    transformed_data = transform_data(x_data)

    model = baseline_model()
    model.fit(transformed_data, y_data, epochs=100)
    return model


def predict(model, data):
    return model.predict(data)


def main():
    # TODO: move all of this to amazon sagemaker

    start_date = datetime(2019, 7, 23, 22, 23, 29)
    model = train(start_date, days=4)

    # raw_data = [{'earlies': 10, 'middays': 20, 'lates': 25},
    #             {'earlies': 50, 'middays': 70, 'lates': 49},
    #             {'earlies': 112, 'middays': 99, 'lates': 109}]

    raw_data = [{'earlies': 113, 'middays': 56, 'lates': 87},
                {'earlies': 22, 'middays': 38, 'lates': 23},
                {'earlies': 68, 'middays': 84, 'lates': 20}]
    data = transform_data(raw_data)

    prediction = predict(model, data)
    print(prediction)  # Should print: [0.83333333, 1.0, 0.77777778]


if __name__ == '__main__':
    main()
