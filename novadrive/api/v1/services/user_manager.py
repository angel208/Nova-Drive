from ..database.user import get_user

def get_user_from_db( id ):
    my_user = get_user(id)
    return my_user
