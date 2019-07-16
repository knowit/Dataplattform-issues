from data_types.AbstractType import AbstractType


class UBWType(AbstractType):
    attributes_keep = {
        ("reg_period", str): ["data", "reg_period"],
        ("used_hours", float): ["data", "used_hrs"]
    }
