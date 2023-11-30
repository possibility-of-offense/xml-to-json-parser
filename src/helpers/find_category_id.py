# Find cat ID
def find_category_id(product, cats):
    get_id = product['id']
    
    for cat in cats:
        if cat.get('product-id').strip().lower() == get_id.strip().lower():
            return cat.get('category-id')