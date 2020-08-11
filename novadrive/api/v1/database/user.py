from . import sql_connection as sql
from mysql.connector.errors import IntegrityError, InterfaceError
from ..utils.errors import ForeignResourceNotFoundException, DBNotConnectedException, ResourceNotFoundException


def get_user( id ):
    try:
        with sql.DBConnection() as sql_connection:
            
            query = "SELECT * FROM user WHERE id = %s"
            val = (id,)

            sql_connection.execute(query, val)
            result = sql_connection.fetchone()

            if not result:
                raise ResourceNotFoundException("User with id '" + str(id) + "' not found.")

            return result

    except IntegrityError as e:
        raise ForeignResourceNotFoundException( e.msg )
    except InterfaceError as e:
        raise DBNotConnectedException()
