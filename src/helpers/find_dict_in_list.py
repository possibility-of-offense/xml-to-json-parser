# Find dictionary in list by key
def find_dict_in_list(l, key):
    for el in l:
        if key in el:
            return el
    
    return False