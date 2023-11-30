# Validate JSON string
def validate_json(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True