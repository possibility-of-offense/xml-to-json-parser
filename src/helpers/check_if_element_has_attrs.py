# Check if element has attributes
def check_if_element_has_attrs(el, attrs):
    conditions = list()

    for attr in attrs:
        if el.find(attr) is not None:
            conditions.append(True)
        else:
            conditions.append(False)

    if len(conditions) == 0 or all(i is True for i in conditions) is False:
        return False

    return True
