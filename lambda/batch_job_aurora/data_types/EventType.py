from data_types.AbstractType import AbstractType


class EventType(AbstractType):
    attributes_keep = {
        ("event_id", str): ["data", "event_id"],
        ("event_name", str): ["data", "event_name"],
        ("event_start", str): ["data", "event_start"],
        ("event_end", str): ["data", "event_end"],
        ("number_of_people", int): ["data", "number_of_people"],
        ("guild", str): ["data", "guild"]
    }
