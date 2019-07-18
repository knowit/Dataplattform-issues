import data_types.EventRatingType as EventRatingType


def test_match_event():
    events = [
        {
            "event_id": "asdf",
            "event_code": "101010",
            "event_name": "test_event",
            "code_valid_from": 0,
            "code_valid_to": 1000,
        },
        {
            "event_id": "asdf2",
            "event_code": "101010",
            "event_name": "test_event2",
            "code_valid_from": 5000,
            "code_valid_to": 99000,
        }
    ]

    def match_event(click):
        return EventRatingType.get_event(click[0], click[1], events=events)

    btnclick1 = ("101010", 50)
    btnclick2 = ("101010", 5001)
    btnclick3 = ("101010", 1001)

    assert match_event(btnclick1)["event_id"] == "asdf"
    assert match_event(btnclick2)["event_id"] == "asdf2"
    assert match_event(btnclick3) is None
