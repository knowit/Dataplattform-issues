import abc


class AbstractType:
    __metaclass__ = abc.ABCMeta

    # This property should be implemented in the classes that extend this class.
    @property
    def attributes_keep(self):
        raise NotImplementedError

    attributes_keep_default = {
        ("id", str): ["id"],
        ("timestamp", int): ["timestamp"]
    }

    def __init__(self):
        self.attributes_keep[("id", str)] = self.attributes_keep_default[("id", str)]
        self.attributes_keep[("timestamp", int)] = self.attributes_keep_default[("timestamp", int)]

    def accept_document(self, doc):
        """
        :param doc: The doc that should be evaluated
        :return: Returns true always here, override the function in the subclass if you only
        want to filter out some records.
        """
        return True

    def accept_row(self, row):
        """
        :param row: The row that should be evaluated. Map of column name -> valye
        :return: Returns true always here, override the function in the subclass if you only
        want to filter out some records.
        """
        return True

    def get_column_values(self, doc):
        """
        :param doc: A raw document from get_docs API.
        :return: a dictionary containing every key, value that you want to insert into Aurora DB.
        """
        output = {}
        for attr, attribute_path in self.attributes_keep.items():
            attr_name = attr[0]
            value = doc.copy()
            is_ok = True

            if len(attr) >= 3:
                # Then we have a special case and we need to run a different function in order
                # to get the values.
                func = attr[2]
                value = func(doc)
                output[attr_name] = value
                continue

            for attr in attribute_path:
                # If the attr is an int, it is actually an index. And therefore we need to
                # make sure that our value list is long enough.
                if type(attr) is int and type(value) is list and attr <= (len(value) - 1):
                    value = value[attr]
                # if not then we need to make sure that attr is a key in the dictionary value.
                elif type(attr) is str and type(value) is dict and attr in value:
                    value = value[attr]
                else:
                    is_ok = False
                    break
            if is_ok:
                output[attr_name] = value
        return output

    def get_create_table_sql(self, table_name):
        """
        :return: A sql string for creating a table for this specific type
        """
        columns_and_types = ""
        for attr in self.attributes_keep.keys():
            attr_name = attr[0]
            attr_type = attr[1]
            if attr_name in ["id", "timestamp"]:
                # We can safely skip the default attributes.
                continue
            if attr_type == str:
                columns_and_types += attr_name + " TEXT,\n"
            elif attr_type == int:
                columns_and_types += attr_name + " INT,\n"
            else:
                print("Unsupported type.")

        sql = f"""
                CREATE TABLE {table_name} (
                    id VARCHAR(24) NOT NULL,
                    timestamp BIGINT NOT NULL,
                    {columns_and_types}
                    PRIMARY KEY (id)
                );
                """
        return sql
