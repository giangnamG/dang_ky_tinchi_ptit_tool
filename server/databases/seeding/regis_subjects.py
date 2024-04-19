import sys
sys.path.append("../")
from core import DB
import base64

def run():
    
    regis_subjects = [
        {
            'major_id' : 'ktdtvt',
            'name_subject' : 'kỹ thuật mạng truyền thông',
            'code_subject' : 'TEL1405',
            'stc' : 3,
            'nam_hoc' : 3,
            'hoc_ky' : 2
        },
        {
            'major_id' : 'ktdtvt',
            'name_subject' : 'kỹ thuật thông tin quang',
            'code_subject' : 'TEL1406',
            'stc' : 3,
            'nam_hoc' : 3,
            'hoc_ky' : 2
        },
        {
            'major_id' : 'ktdtvt',
            'name_subject' : 'kỹ thuật thông tin vô tuyến',
            'code_subject' : 'TEL1407',
            'stc' : 3,
            'nam_hoc' : 3,
            'hoc_ky' : 2
        },
        {
            'major_id' : 'ktdtvt',
            'name_subject' : 'Hệ điều hành',
            'code_subject' : 'TEL1339',
            'stc' : 2,
            'nam_hoc' : 3,
            'hoc_ky' : 2
        },
        {
            'major_id' : 'ktdtvt',
            'name_subject' : 'Cấu trúc dữ liệu và giải thuật',
            'code_subject' : 'TEL1342',
            'stc' : 3,
            'nam_hoc' : 3,
            'hoc_ky' : 2
        },
        {
            'major_id' : 'ktdtvt',
            'name_subject' : 'Công nghệ phần mềm',
            'code_subject' : 'TEL1341',
            'stc' : 3,
            'nam_hoc' : 3,
            'hoc_ky' : 2
        },
        {
            'major_id' : 'ktdtvt',
            'name_subject' : 'kỹ thuật thông tin quang',
            'code_subject' : 'TEL1406',
            'stc' : 3,
            'nam_hoc' : 3,
            'hoc_ky' : 2
        }
    ]
    query = """
        insert into regis_subjects 
        (major_id,name_subject, code_subject, stc, nam_hoc, hoc_ky)
        values (%s,%s, %s, %s, %s, %s)
        """
    username = "ngn"
    password = base64.b64encode("ngn@ngn".encode("utf-8"))
    
    DB().insert_data(query, params=(username, password, '', '', 1))
        