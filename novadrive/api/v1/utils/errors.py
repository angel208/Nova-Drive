import re

class ForeignResourceNotFoundException(Exception):

    def __init__(self, sql_message = None):

        if( sql_message != None ):

            message = "{} with given id doesn't exists"

            resource = re.search( 'REFERENCES `(.*)` \(', sql_message ).group(1).title()

            self.message = message.format(resource)
            
        else:

            self.message = "Resource not found in the Database"

        super().__init__(self.message)



class DBNotConnectedException(Exception):

    def __init__(self, message="The database is not connected"):
        self.message = message
        super().__init__(self.message)



class S3StoreException(Exception):

    def __init__(self, message="Could not upload to S3"):
        self.message = message
        super().__init__(self.message)



def find_error( marshmallow_error ):

    missing_required_field = any('Missing data for required field.' in val for val in marshmallow_error.values())

    if(missing_required_field):
        return marshmallow_error

    return None