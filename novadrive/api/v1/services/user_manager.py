from ..database.user import get_user

def get_user_data( id ):
    my_user = get_user(id)
    return my_user
