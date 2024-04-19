import sys
sys.path.append(r'../')
from core import DB

def run():
        DB().drop("regis_subjects")
        query = """create table if not exists regis_subjects(
                id integer primary key auto_increment not null, 
                major_id integer,
                name_subject varchar(50) not null,
                code_subject varchar(10) not null,
                stc integer,
                nam_hoc integer,
                hoc_ky integer)
                """
        DB().create_table(query)