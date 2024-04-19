import sys
sys.path.append(r'../')
from core import DB

def run():
        DB().drop("users")
        query = """create table if not exists users 
                (id integer primary key auto_increment not null,
                username varchar(30) not null unique,
                password varchar(200) not null,
                username_qldt varchar(30),
                password_qldt varchar(50),
                role_id integer,
                status_access_qldt integer default 0)
                """
        DB().create_table(query)