from . import sql_connection as sql


def create_folder( name, parent_id, owner_id ):

    with sql.DBConnection() as sql_connection:
        
        query = "INSERT INTO folder (name, parent_id, owner_id) VALUES (%s, %s, %s)"
        val = (name, parent_id, owner_id)

        sql_connection.execute(query, val)
        inserted_row_id = sql_connection.lastrowid

        return inserted_row_id

def get_folder( id ):

    with sql.DBConnection() as sql_connection:
        
        query = "SELECT * FROM folder WHERE id = %s"
        val = (id, )

        sql_connection.execute(query, val)
        result = sql_connection.fetchone()

        return result


