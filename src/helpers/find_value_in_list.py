# Find value in list
def find_in_list(list, value):
    for val in list:
        if val in value:
            return True
    
    return False