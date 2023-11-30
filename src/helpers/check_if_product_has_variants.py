# Check if the product has variations but not variants
def check_if_product_has_variants(product):
    if product.find('variations') and sum(1 for e in product.iter('variants')) > 0:
        return True
    elif product.find('variations') and sum(1 for e in product.iter('variants')) == 0:
        return False

    return True