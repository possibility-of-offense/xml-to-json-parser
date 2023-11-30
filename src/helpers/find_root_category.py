# Find root category
def find_root_category(categories, cat):
    found_category = ''
    cat_id = ''

    for category in categories:
        if category.get('category-id') == cat and category.find('display-name').text in categories:
            found_category = category.find('display-name').text

        if category.get('category-id') == cat:
            if category.find('parent').text:
                cat_id = category.find('parent').text

                if cat_id == 'root':
                    return category.find('display-name').text

    if found_category != '':
        return found_category
    
    found_category = find_root_category(categories, cat_id)
    return found_category
