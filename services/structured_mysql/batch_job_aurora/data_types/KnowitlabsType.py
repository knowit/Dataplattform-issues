from data_types.AbstractType import AbstractType


class KnowitlabsType(AbstractType):
    attributes_keep = {
        ("title", str): ["data", "title"],
        ("subtitle", str): ["data", "subtitle"],
        ("created", int): ["data", "created"],
        ("author", str): ["data", "author"]
    }
