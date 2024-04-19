import sys
sys.path.append(r'../')
from core import DB

def run():
        DB().drop("roles")
        query = """create table if not exists roles 
                (id integer primary key auto_increment not null, 
                role_name varchar(10))
                """
        DB().create_table(query)