import sys
sys.path.append(r'../')
from core import DB

def run():
    DB().drop("record_subject_to_regis")
    query = """create table if not exists record_subject_to_regis(
            id integer primary key auto_increment, 
            code_subject varchar(10) not null,
            name_subject varchar(255) not null,
            group_name varchar(10) not null,
            team_name varchar(10) not null,
            stc integer not null,
            user_id integer not null,
            signed integer default 0
            )
            """
    DB().create_table(query)