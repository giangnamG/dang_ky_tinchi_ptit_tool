import sys, os
sys.path.append("./clone")
sys.path.append("../")
from clone import main
from core import DB

def run():
    attt_major_subjects = main.get(os.path.join(os.path.dirname(__file__),'clone/ATTT.txt'))
    query = """
        insert into subjects 
        (nameSubject, codeSubject, stc, major_id)
        values (%s, %s, %s, %s)
        """
    id_major = int(DB().select_data("select id from majors where type = 'attt'", params=None)[0][0])
    for subject in attt_major_subjects:
        DB().insert_data(query, params=(
            subject['NameSubjects'],
            subject['CodeSubjects'],
            subject['STC'],
            id_major,
        ))
        