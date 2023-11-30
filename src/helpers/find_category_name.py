from helpers.retrieve_value import retrieve_value
from helpers.find_root_category import find_root_category

# Find cat name
def find_category_name(categories, cat_id, dictionary):
    for cat in categories:
        if cat.get('category-id') == cat_id:
            if cat.find('parent').text == 'root':
                for child in cat:
                    if child.tag == 'display-name':
                        if 'category' not in dictionary:
                            return retrieve_value(child)
            else:
                if 'category' not in dictionary:
                    dictionary['category'] = cat.find('display-name').text

                get_parent = find_root_category(categories, cat.find('parent').text)
                
                return get_parent