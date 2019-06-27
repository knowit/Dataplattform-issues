from data_types.AbstractType import AbstractType


class EventRatingType(AbstractType):
    attributes_keep = {
        ("button", int): ["data", "button"]
    }
