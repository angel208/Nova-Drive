from . import sql_connection as sql



def get_user( id ):

    with sql.DBConnection() as sql_connection:
        
        query = "SELECT * FROM user WHERE id = %s"
        val = (id,)

        sql_connection.execute(query, val)
        result = sql_connection.fetchone()

        return result

