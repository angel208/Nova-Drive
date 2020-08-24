from . import sql_connection as sql
from mysql.connector.errors import IntegrityError, InterfaceError
from ..utils.errors import ForeignResourceNotFoundException, DBNotConnectedException, ResourceNotFoundException

def store_file_in_db( name, filetype, folder_id, user_id, internal_filename, file_uri = 'unassigned', thumbnail_uri = 'unassigned' , filesize = 0, md5 = ''):

    try:

        with sql.DBConnection() as sql_connection:
            
            query = "INSERT INTO file (name, type, folder_id,  user_id, internal_filename, file_uri, thumbnail_uri, filesize, md5  ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (name, filetype , folder_id, user_id, internal_filename, file_uri, thumbnail_uri, filesize, md5)

            
            sql_connection.execute(query, val)
            inserted_row_id = sql_connection.lastrowid

            return inserted_row_id
    
    except IntegrityError as e:
        raise ForeignResourceNotFoundException( e.msg )
    except InterfaceError as e:
        raise DBNotConnectedException()




def get_file( id ):

    try:
        with sql.DBConnection() as sql_connection:
            
            query = "SELECT * FROM file WHERE id = %s AND deleted IS %s"
            val = (id, None)

            sql_connection.execute(query, val)
            result = sql_connection.fetchone()

            if not result:
                raise ResourceNotFoundException("File with id '" + str(id) + "' not found.")

            return result

    except IntegrityError as e:
        raise ForeignResourceNotFoundException( e.msg )
    except InterfaceError as e:
        raise DBNotConnectedException()
    

def soft_delete_file( id ):

    try:
        with sql.DBConnection() as sql_connection:
            
            query = "UPDATE file SET deleted = NOW() WHERE id = %s"
            val = ( id, )

            sql_connection.execute(query, val)

            affected_rows = sql_connection.rowcount
            
            if( affected_rows == 0 ):
                raise ResourceNotFoundException("File with id '" + str(id) + "' not found.")

            return affected_rows

    except InterfaceError as e:
        raise DBNotConnectedException()
