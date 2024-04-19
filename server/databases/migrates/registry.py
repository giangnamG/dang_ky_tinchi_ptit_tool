import sys, os
sys.path.append(os.path.dirname(__file__))
import table_subject, table_user, table_major \
    , table_role, dky_tin, table_record_subject_to_regis

def up():
    table_subject.run()
    table_user.run()
    table_major.run()
    table_role.run()
    dky_tin.run()
    table_record_subject_to_regis.run()