import sys, os
sys.path.append("../")
from core import DB

def run():
    DB().drop('majors')
    query = """
        create table if not exists majors(
        id integer primary key auto_increment,
        name_major varchar(100) not null,
        type varchar(100) not null)
        """
    DB().create_table(query=query)