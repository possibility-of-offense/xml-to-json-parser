# Merge dictionaries
def merge_dictionaries(current_dictionary, original_dictionary, id):
    """
        current_dictionary is the dictionary at the which the loop is just iterating
        original_dictionary is the dictionary already exists in products_info and to be merged with
    """

    for i, v in current_dictionary[id].items():
        if i not in original_dictionary[id]:
            original_dictionary[id][i] = v
        else:
            original_dictionary[id][i].extend(v)
