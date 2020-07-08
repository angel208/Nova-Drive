from . import sql_connection as sql
from mysql.connector.errors import IntegrityError, InterfaceError
from ..utils.errors import ForeignResourceNotFoundException, DBNotConnectedException

def store_file_in_db( name, filetype, folder_id, user_id, file_uri, thumbnail_uri = '' , filesize = 0):

    try:

        with sql.DBConnection() as sql_connection:
            
            query = "INSERT INTO file (name, type, folder_id, user_id, file_uri, thumbnail_uri, filesize  ) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (name, filetype , folder_id, user_id, file_uri, thumbnail_uri, filesize)

            
            sql_connection.execute(query, val)
            inserted_row_id = sql_connection.lastrowid

            return inserted_row_id
    
    except IntegrityError as e:
        raise ForeignResourceNotFoundException( e.msg )
    except InterfaceError as e:
        raise DBNotConnectedException()


def get_file( id ):

    with sql.DBConnection() as sql_connection:
        
        query = "SELECT * FROM file WHERE id = %s AND deleted IS %s"
        val = (id, None)

        sql_connection.execute(query, val)
        result = sql_connection.fetchone()

        return result

def soft_delete_file( id ):

    with sql.DBConnection() as sql_connection:
        
        query = "UPDATE file SET deleted = NOW() WHERE id = %s"
        val = ( id, )

        sql_connection.execute(query, val)
        
        return sql_connection.rowcount

