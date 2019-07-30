from data_types.AbstractType import AbstractType


class DayRatingType(AbstractType):
    attributes_keep = {
        ("button", int): ["data", "button"]
    }
