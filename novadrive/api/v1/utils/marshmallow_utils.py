def find_error( marshmallow_error ):

    missing_required_field = any('Missing data for required field.' in val for val in marshmallow_error.values())

    if(missing_required_field):
        return marshmallow_error

    return None