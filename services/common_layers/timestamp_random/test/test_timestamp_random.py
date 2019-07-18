import timestamp_random


def test_get_timestamp_without_random_sorted():
    # This test creates a couple of timestamp random ids which should be in sorted order because
    # they have no random value and the time is ascending.
    timestamp_random_list = []
    for time in range(1, 100):
        random_timestamp = timestamp_random.get_timestamp_random(timestamp=time, random_value=0)
        timestamp_random_list.append(random_timestamp)

    for i in range(1, len(timestamp_random_list)):
        assert timestamp_random_list[i - 1] < timestamp_random_list[i]


def test_get_timestamp_random_sorted():
    # Should also be in sorted order even when there is randomness involved because the timestamp
    # is different for each one.
    timestamp_random_list = []
    for time in range(1, 100):
        random_timestamp = timestamp_random.get_timestamp_random(timestamp=time)
        timestamp_random_list.append(random_timestamp)

    for i in range(1, len(timestamp_random_list)):
        assert timestamp_random_list[i - 1] < timestamp_random_list[i]


def test_get_timestamp_random_with_correct_timestamps():
    # Here the real timestamps are used which means that these can be created at the exact same
    # timestamp, therefore we need to have no random values and check if it is less than OR equal.
    timestamp_random_list = []
    for time in range(1, 100):
        random_timestamp = timestamp_random.get_timestamp_random(random_value=0)
        timestamp_random_list.append(random_timestamp)

    for i in range(1, len(timestamp_random_list)):
        assert timestamp_random_list[i - 1] <= timestamp_random_list[i]


def test_get_range_timestamp_random():
    timestamp = 123456789
    low, high = timestamp_random.get_range_timestamp_random(timestamp)
    assert low == b'\x00\x00pH\x86\r\xaf@\x00\x00\x00\x00\x00\x00\x00\x00'
    assert high == b'\x00\x00pH\x86\x1c\xf1\x80\x00\x00\x00\x00\x00\x00\x00\x00'
