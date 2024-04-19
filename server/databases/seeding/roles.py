import sys
sys.path.append("../")
from core import DB

def run():
    query = """
        insert into roles 
        (role_name)
        values (%s)
        """
    roles = ['admin', 'user']
    
    DB().insert_data(query, params=(roles[0],))
    DB().insert_data(query, params=(roles[1],))
        