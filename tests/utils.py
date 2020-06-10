from novadrive.api.v1.database import sql_connection as sql

def db_init( ):
    print("\ninit db...\n")

    with sql.DBConnection( testing = True ) as sql_connection:
        
        query = "INSERT INTO user (name, lastname, email, storage_remaining, password ) VALUES ( %s, %s, %s, %s, %s); "
        val = ("test", "user", "angel.pena@gmail.com", "10000000", "5F4DCC3B5AA765D61D8327DEB882CF99",)

        sql_connection.execute(query, val)

    return

def db_cleanup( ):
    print("\ncleanup db")
    
    with sql.DBConnection( testing = True ) as sql_connection:
        
        query =  """ SET FOREIGN_KEY_CHECKS = 0; 
                     TRUNCATE TABLE shared; 
                     ALTER TABLE shared AUTO_INCREMENT = 1;
                     TRUNCATE TABLE login; 
                     ALTER TABLE login AUTO_INCREMENT = 1;
                     TRUNCATE TABLE api_log;
                     ALTER TABLE api_log AUTO_INCREMENT = 1;
                     TRUNCATE TABLE folder; 
                     ALTER TABLE folder AUTO_INCREMENT = 1;
                     TRUNCATE TABLE file; 
                     ALTER TABLE file AUTO_INCREMENT = 1;
                     TRUNCATE TABLE user;
                     ALTER TABLE user AUTO_INCREMENT = 1;
                     
                     SET FOREIGN_KEY_CHECKS = 1; """ 

        

        results = sql_connection.execute(query,  multi=True)
        
        for cur in results:
            print('cursor:', cur)
            if cur.with_rows:
                print('result:', cur.fetchall())
                

        print("cleaned up db")

    return 1