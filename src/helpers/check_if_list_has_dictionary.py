# Check if the list has a certain dictionary by comparing the values from the keys_list with the dict_key
def check_if_list_has_dict(keys_list, dict_key):
    for item in keys_list:
        if type(item) == dict:
            if dict_key in item:
                return True

    return False