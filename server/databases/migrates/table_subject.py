import sys, os
sys.path.append("../")
from core import DB

def run():
    DB().drop("subjects")
    query = """create table if not exists subjects
    (id integer primary key auto_increment,
    nameSubject varchar(100) not null,
    codeSubject varchar(20) not null,
    stc integer,
    major_id integer)
    """
    DB().create_table(query=query)