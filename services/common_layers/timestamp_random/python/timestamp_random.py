import random
from datetime import datetime as dt


def get_timestamp_random(timestamp=None, random_value=None):
    """
    :param random_value: You can choose a specific value instead of generating a random one.
    :param timestamp: A specific unix timestamp, keep None if you want to use current time.
    :return: timestamp in bits appended with some random bits as a Binary.
    """

    def to_byte_array(number: int, bytes: int = 16):
        return number.to_bytes(bytes, 'big')

    if timestamp is None:
        timestamp = int(dt.now().timestamp() * 1_000_000)
    else:
        timestamp *= 1_000_000

    if random_value is None:
        random_value = random.getrandbits(64)

    return to_byte_array((timestamp << 64) + random_value, 16)


def get_range_timestamp_random(timestamp: int):
    """
    :param timestamp: Unix timestamp
    :return: A range of possible values a timestamp can get from get_timestamp_random().
    """

    lowest = get_timestamp_random(timestamp, random_value=0)
    highest = get_timestamp_random(timestamp + 1, random_value=0)
    return lowest, highest
