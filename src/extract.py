import xml.etree.ElementTree as ET
import json
import os
import sys

rootpath = os.path.join(os.getcwd(), '..')
sys.path.append(rootpath)

# tree = ET.parse('./xml/master.xml')
tree = ET.parse('./xml/test.xml')
root = tree.getroot()

# List to append all dictionaries
products_info = []
test = 1

# Keys in XML to help retrieve information
xml_keys = ['display-name', 'short-description', 'long-description', 'online-flag', 'available-flag',
    {'custom-attributes': ['category', 'categoryGroup', 'composition', 'detailedRefinementCategory', 'suggestedRetailPrice']},
    {'variations':  ['color', 'size']}
]

# Necessary keys in XML to start retrieving information
mandatory_xml_keys = ['display-name', 'online-flag', 'available-flag']

# Top-category names (gender)
top_category_names = ['Man', 'Woman', 'Unisex']

# Variables
product_id = 'product-id'
attribute_id_key = 'attribute-id'
variation_attribute_values_key = 'variation-attribute-values'

# Helper functions
from helpers.retrieve_value import retrieve_value
from helpers.initialize_dictionary import init_dict
from helpers.find_value_in_list import find_in_list
from helpers.validate_json import validate_json
from helpers.check_if_element_has_attrs import check_if_element_has_attrs
from helpers.find_category_id import find_category_id
from helpers.find_root_category import find_root_category
from helpers.find_category_name import find_category_name
from helpers.check_if_list_has_dictionary import check_if_list_has_dict
from helpers.check_if_product_has_variants import check_if_product_has_variants

# Main

categories = root.findall('category')
category_assignments = root.findall('category-assignment')
products = [elem for elem in root.iter('product')]

for product in products:
    product_dict = dict()

    if check_if_product_has_variants(product) is False:
        continue

    # Check if the product has one of the mandatory XML keys/tags with attributes
    if check_if_element_has_attrs(product, mandatory_xml_keys) is True:
        init_dict(product_dict, product.get(product_id))
        
        # Find cat id
        cat_id = find_category_id(product_dict, category_assignments)
        cat_name = find_category_name(categories, cat_id, product_dict)

        # Check if cat_name exists in top_category_names and set it in product_dict as gender
        if cat_name and cat_name in top_category_names:
            product_dict['gender'] = cat_name

        for product_child in product:
            product_child_tag = product_child.tag.lower()

            # Check if the nested XML tag exists in the list
            if product_child_tag in xml_keys:
                product_dict[product_child_tag] = retrieve_value(product_child)
            
            if check_if_list_has_dict(xml_keys, product_child_tag):
                for key in xml_keys:
                    if product_child_tag in key:
                        # Get filter from the list
                        get_filters = key[product_child_tag]

                        # Create an empty list
                        product_dict[product_child_tag] = list()

                        # If we are traversing a custom-attributes
                        if product_child_tag == 'custom-attributes':
                            for product_child_children in product_child:
                                product_child_children_attrs = list(product_child_children.attrib.items())

                                for i, v in product_child_children_attrs:
                                    if v in get_filters:
                                        if 'lang' in product_child_children_attrs or '{http://www.w3.org/XML/1998/namespace}lang' in product_child_children_attrs:
                                            product_dict[product_child_tag].append(product_child_children.text)
                                        else:
                                            product_dict[product_child_tag].append(product_child_children.text)

                        # If we are traversin a variations
                        if product_child_tag == 'variations':

                            # Check if there are any variants
                            if sum(1 for e in product_child.iter('variants')) > 0:
                                # Get variants
                                variants = product_child.iter('variant')

                                for val in [elem for elem in product_child.iter('variation-attribute')]:
                                    if val.attrib[attribute_id_key] in get_filters:
                                        
                                        # Loop through variation-attribute-values
                                        if val.find(variation_attribute_values_key):
                                            for var_attr in val.find(variation_attribute_values_key):
                                                
                                                variant_dict = dict()

                                                for variant in variants:
                                                    variant_id = variant.get('product-id')
                                                    get_variant_product = root.find('./product/[@product-id="' + variant_id + '"]')
                                                    
                                                    if get_variant_product is not None:
                                                        variant_custom_attrs = get_variant_product.iter('custom-attribute')
                                                        
                                                        for attr in variant_custom_attrs:
                                                            if attr.get('attribute-id') in get_filters:
                                                                if attr.text == var_attr.get('value'):
                                                                    variant_dict[variant_id] = {
                                                                        attr.get('attribute-id'): [attr.text]
                                                                    }
                                                                    print(variant_dict)
                                                
                                                if len(variant_dict) > 0:
                                                    product_dict[product_child_tag].append(variant_dict)
    if len(product_dict) > 0:   
        products_info.append(product_dict)

json_data = json.dumps({"products": products_info}, indent = 4)

with open('../dist/test.json', 'w') as file:
# # with open('../dist/master.json', 'w') as file:
    file.write(json_data)