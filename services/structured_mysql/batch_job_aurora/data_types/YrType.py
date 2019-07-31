from data_types.AbstractType import AbstractType


class YrType(AbstractType):
    attributes_keep = {
        ("location", str): ["data", "location"],
        ("location_name", str): ["data", "location_name"],
        ("time_from", int): ["data", "time_from"],
        ("time_to", int): ["data", "time_to"],
        ("precipitation", float): ["data", "precipitation"],
        ("wind_speed", float): ["data", "wind_speed"],
        ("temperature", int): ["data", "temperature"],
        ("air_pressure", float): ["data", "air_pressure"]
    }
