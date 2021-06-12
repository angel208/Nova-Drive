from ..database.user import get_user, user_exists
from ..utils.errors import UserAlreadyExistsException
from passlib.hash import pbkdf2_sha256 as sha256

def get_user_data( id ):
    my_user = get_user(id)
    return my_user

def create_user( request_data ):

    #data format: {'unername' , 'password', 'email', 'password_confirmation' }
    password = request_data['password']
    email = request_data['email']

    #verify that user does not exists
    if user_exists( email ):
        raise UserAlreadyExistsException()

    #create root folder
    

    #generate password
    hashed_password = generate_hash(password)
    print(hashed_password)

    #store folder info in db
    # created_user_id = store_folder_in_db(   name = folder_name, 
    #                                         parent_id = parent_id, 
    #                                         owner_id = user_id )

    #return get_user( created_user_id )
    # 'access_token': access_token,
    # 'refresh_token': refresh_token
    return request_data


def generate_hash(password):
    return sha256.hash(password)    
    
def verify_hash(password, hash):
    return sha256.verify(password, hash)