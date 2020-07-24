from . import sql_connection as sql
from mysql.connector.errors import IntegrityError, InterfaceError
from ..utils.errors import ForeignResourceNotFoundException, DBNotConnectedException, ResourceNotFoundException


def store_folder_in_db( name, parent_id, owner_id ):

    try:
        with sql.DBConnection() as sql_connection:
            
            query = "INSERT INTO folder (name, parent_id, owner_id) VALUES (%s, %s, %s)"
            val = (name, parent_id, owner_id)

            sql_connection.execute(query, val)
            inserted_row_id = sql_connection.lastrowid

            return inserted_row_id

    except IntegrityError as e:
        raise ForeignResourceNotFoundException( e.msg )
    except InterfaceError as e:
        raise DBNotConnectedException()

def get_folder( folder_id ):

    try:

        with sql.DBConnection() as sql_connection:
            
            query = "SELECT * FROM folder WHERE id = %s AND deleted IS %s"
            val = (folder_id, None)

            sql_connection.execute(query, val)
            result = sql_connection.fetchone()

            if not result:
                raise ResourceNotFoundException("Folder with id '" + str(folder_id) + "' not found.")

            return result

    except IntegrityError as e:
        raise ForeignResourceNotFoundException( e.msg )
    except InterfaceError as e:
        raise DBNotConnectedException()


def soft_delete_folder( folder_id ):

    with sql.DBConnection() as sql_connection:
        
        #This query sets the folder "deleted" column to the current date
        #it also updates all the child folders in its hierachy 
        #credits to https://stackoverflow.com/questions/41913460/mysql-recursive-get-all-child-from-parent
        query = """
                UPDATE folder  
                JOIN (  select * from 
                            (select * from folder order by parent_id, id) folder,         
                            (select @pv := '%s') initialisation 
                        where @pv = id
                        or ( find_in_set(parent_id, @pv) > 0 and @pv := concat(@pv, ',', id) ) 
                    ) childs 
                ON (folder.id = childs.id) 
                SET folder.deleted = now()
                """

        val = ( folder_id, )

        sql_connection.execute(query, val)
        
        affected_rows = sql_connection.rowcount
            
        if( affected_rows == 0 ):
            raise ResourceNotFoundException("Folder with id '" + str(folder_id) + "' not found.")

        return affected_rows



def list_child_folders( folder_id ):
    
    try:

        with sql.DBConnection() as sql_connection:
            
            query = "SELECT * FROM folder WHERE parent_id = %s AND deleted IS %s"
            val = (folder_id, None)

            sql_connection.execute(query, val)
            result = sql_connection.fetchall()

            if not result:
                raise ResourceNotFoundException("Folder with id '" + str(folder_id) + "' not found.")

            return result
        
    except IntegrityError as e:
        raise ForeignResourceNotFoundException( e.msg )
    except InterfaceError as e:
        raise DBNotConnectedException()
    
        
def list_files_of_folder( folder_id ):
    
    try:

        with sql.DBConnection() as sql_connection:
            
            query = "SELECT * FROM file WHERE folder_id = %s AND deleted IS %s"
            val = (folder_id, None)

            sql_connection.execute(query, val)
            result = sql_connection.fetchall()

            if not result:
                raise ResourceNotFoundException("Folder with id '" + str(folder_id) + "' not found.")

            return result

    except IntegrityError as e:
        raise ForeignResourceNotFoundException( e.msg )
    except InterfaceError as e:
        raise DBNotConnectedException()


