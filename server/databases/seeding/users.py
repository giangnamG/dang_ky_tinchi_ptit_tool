import sys
sys.path.append("../")
from core import DB
import base64

def run():
    query = """
        insert into users 
        (username, password, username_qldt, password_qldt, role_id)
        values (%s, %s, %s, %s, %s)
        """
    username = "ngn"
    password = base64.b64encode("ngn@ngn".encode("utf-8"))
    DB().insert_data(query, params=(username, password, '', '', 1))
    
    username = "b21dcat014"
    password = base64.b64encode("ngn@ngn".encode("utf-8"))
    DB().insert_data(query, params=(username, password, '', '', 1))
        