class AbstractType:

    def get_column_values(self, doc):
        """
        :param doc: A raw document from get_docs API.
        :return: a dictionary containing every key, value that you want to insert into Aurora DB.
        """
        output = {}
        for attr_name, attribute_path in self.attributes_keep.items():
            value = doc.copy()
            is_ok = True
            for attr in attribute_path:
                # If the attr is an int, it is actually an index. And therefore we need to
                # make sure that our value list is long enough.
                if type(attr) is int and attr <= (len(value) - 1):
                    value = value[attr]
                # if not then we need to make sure that attr is a key in the dictionary value.
                elif type(attr) is str and attr in value:
                    value = value[attr]
                else:
                    is_ok = False
                    break
            if is_ok:
                output[attr_name] = value
        return output
