from . import sql_connection as sql


def create_folder( name, parent_id, owner_id ):

    with sql.DBConnection() as sql_connection:
        
        query = "INSERT INTO folder (name, parent_id, owner_id) VALUES (%s, %s, %s)"
        val = (name, parent_id, owner_id)

        sql_connection.execute(query, val)
        inserted_row_id = sql_connection.lastrowid

        return inserted_row_id

def get_folder( folder_id ):

    with sql.DBConnection() as sql_connection:
        
        query = "SELECT * FROM folder WHERE id = %s AND deleted IS %s"
        val = (folder_id, None)

        sql_connection.execute(query, val)
        result = sql_connection.fetchone()

        return result

def soft_delete_folder( folder_id ):

    with sql.DBConnection() as sql_connection:
        
        query = "UPDATE folder SET deleted = NOW() WHERE id = %s"
        val = ( folder_id, )

        sql_connection.execute(query, val)
        
        return sql_connection.rowcount

def list_child_folders( folder_id ):
    
    with sql.DBConnection() as sql_connection:
        
        query = "SELECT * FROM folder WHERE parent_id = %s AND deleted IS %s"
        val = (folder_id, None)

        sql_connection.execute(query, val)
        result = sql_connection.fetchall()

        return result
        
def list_files_of_folder( folder_id ):
    
    with sql.DBConnection() as sql_connection:
        
        query = "SELECT * FROM file WHERE folder_id = %s AND deleted IS %s"
        val = (folder_id, None)

        sql_connection.execute(query, val)
        result = sql_connection.fetchall()

        return result


