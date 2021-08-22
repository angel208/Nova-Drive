from . import sql_connection as sql
from mysql.connector.errors import IntegrityError, InterfaceError
from ..utils.errors import ForeignResourceNotFoundException, DBNotConnectedException, ResourceNotFoundException
from datetime import datetime

def store_file_in_db( name, filetype, folder_id, user_id, internal_filename, thumbnail_uri = 'unassigned' , filesize = 0, md5 = ''):

    try:

        with sql.DBConnection() as sql_connection:
            
            query = "INSERT INTO file (name, type, folder_id,  user_id, internal_filename, thumbnail_uri, filesize, md5  ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (name, filetype , folder_id, user_id, internal_filename, thumbnail_uri, filesize, md5)

            
            sql_connection.execute(query, val)
            inserted_row_id = sql_connection.lastrowid

            return inserted_row_id
    
    except IntegrityError as e:
        raise ForeignResourceNotFoundException( e.msg )
    except InterfaceError as e:
        raise DBNotConnectedException()




def get_file_data( id ):

    try:
        with sql.DBConnection() as sql_connection:
            
            query = "SELECT file.* FROM file, folder WHERE file.folder_id = folder.id AND file.id = %s AND file.deleted IS  %s AND folder.deleted IS  %s"
            val = (id, None, None)

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
            
            query = "UPDATE file SET deleted = NOW(3) WHERE id = %s"
            val = ( id, )

            sql_connection.execute(query, val)

            affected_rows = sql_connection.rowcount
            
            if( affected_rows == 0 ):
                raise ResourceNotFoundException("File with id '" + str(id) + "' not found.")

            return affected_rows

    except InterfaceError as e:
        raise DBNotConnectedException()

def rename_file( id, new_name ):

    try:
        with sql.DBConnection() as sql_connection:
            
            query = """ UPDATE file
                        INNER JOIN folder ON 
                            file.folder_id = folder.id AND 
                            folder.deleted IS %s 
                        SET file.name = %s, file.updated = NOW(3)
                        WHERE file.id = %s 
                        AND   file.deleted IS %s """

            val = (None, new_name, id, None )

            sql_connection.execute(query, val)

            affected_rows = sql_connection.rowcount
            
            if( affected_rows == 0 ):
                raise ResourceNotFoundException("File with id '" + str(id) + "' not found.")

            return affected_rows

    except InterfaceError as e:
        raise DBNotConnectedException()
        

def move_file( id, new_folder ):

    try:
        with sql.DBConnection() as sql_connection:
            
            query = """ UPDATE file
                        INNER JOIN folder ON 
                            file.folder_id = folder.id AND 
                            folder.deleted IS %s 
                        SET file.folder_id = %s, file.updated = NOW(3) 
                        WHERE file.id = %s 
                        AND   file.deleted IS %s """

            val = (None, new_folder, id, None )

            sql_connection.execute(query, val)

            affected_rows = sql_connection.rowcount
            
            if( affected_rows == 0 ):
                raise ResourceNotFoundException("File with id '" + str(id) + "' not found.")

            return affected_rows

    except InterfaceError as e:
        raise DBNotConnectedException()