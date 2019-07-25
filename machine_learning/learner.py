import tensorflow
from data_fetcher import DataFetcher
from datetime import datetime


def main():
    # TODO: move all of this to amazon sagemaker
    # Usually just use the date for today.
    july24 = datetime(2019, 7, 24, 19, 23, 29)
    print(DataFetcher.fetch_daily_data(july24))


if __name__ == '__main__':
    main()
