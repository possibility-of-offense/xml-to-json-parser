# Retrieve value based on lang attribute
def retrieve_value(child):
    if 'lang' in child.attrib and child.attrib['lang'].lower() == 'en':
        return child.text
    if '{http://www.w3.org/XML/1998/namespace}lang' in child.attrib and child.attrib['{http://www.w3.org/XML/1998/namespace}lang'].lower() == 'en':
        return child.text
    
    return child.text