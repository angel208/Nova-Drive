from . import sql_connection as sql


def create_file( name, filetype, folder_id, user_id, file_uri, thumbnail_uri = '' , filesize = 0):

    with sql.DBConnection() as sql_connection:
        
        query = "INSERT INTO file (name, type, folder_id, user_id, file_uri, thumbnail_uri, filesize  ) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (name, filetype , folder_id, user_id, file_uri, thumbnail_uri, filesize)

        sql_connection.execute(query, val)
        inserted_row_id = sql_connection.lastrowid

        return inserted_row_id


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

