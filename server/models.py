from databases.core import DB
import base64
from datetime import datetime

class User:
    def __init__(self):
        pass
    
    def check_user_already_exists(self,username, password):
        password = base64.b64encode(password)
        user = DB().select_data('select * from users where username=%s and password=%s', (username, password))
        if len(user) > 0:
            return {
                'status': True,
                'result': user[0]
                }
        return {
                'status': False,
                'result': None
                }
    def update_account_qldt(self,username, username_qldt, password_qldt):
        DB().update('update users set username_qldt=%s,password_qldt=%s where username=%s',(username_qldt, password_qldt,username))
    def updateIsOnline(self,username,isOnline):
        DB().update('update users set isOnline=%s where username=%s',(isOnline,username))   
    def GetRole(self, username, password):
        password = base64.b64encode(password)
        role_name = DB().select_data('select role_name from roles where id = (select role_id from users where username=%s and password=%s)', (username, password))
        if len(role_name) > 0:
            return role_name[0][0]
        return None
        '''
            return integer or None
        '''
    
    def set_status_access_qldt(self,isAccessTokenQLDT, username):
        # user = DB().select_data('select id from users where username=%s', (username,))
        # if len(user) > 0:
        #     DB().update("update users set status_access_qldt = %s where username = %s",(isAccessTokenQLDT,username))
        #     return {
        #         'status': True,
        #         'Message': 'Updated'
        #     }
        # return {
        #     'status': False,
        #     'Message': 'Username invalid'
        # }
        DB().update("update users set status_access_qldt = %s where username = %s",(isAccessTokenQLDT,username))
        return {
            'status': True,
            'Message': 'Updated'
        }
    def FetchALlUsers(self):
        return DB().select_data('select * from users',())
    def CreateUser(self, username,password):
        password = base64.b64encode(password.encode())
        user = DB().select_data('select * from users where username=%s and password=%s',(username,password))
        if len(user) > 0:
            return {
                'result': False,
                'Message': 'user already exists'
            }
        else:
            DB().insert_data('insert into users (username,password,role_id) values (%s,%s,2)',(username,password))
            return {
                'result': True,
                'Message': 'create success'
            }
class Majors():
    
    def get_majors_title(self):
        '''
            :return tuples in array
        '''
        return DB().select_data(query="select * from majors", params=None)
        
    def findSubjectWithCode(self,codeSubject,group_number,team_number):
        subject = DB().select_data('select * from ds_nhom_to where ma_mon=%s and group_number=%s and team_number=%s', (codeSubject,group_number,team_number))
        if len(subject) == 0:
            return None        
        return subject[0]
    
    def get_subjects_depend_major(self,major):
        if major == '':
            major = 'default'
        results = DB().select_data(query="select * from subjects where major_id = (select id from majors where type = %s)", params=(major,))
        if results is not None:
            subjects = [
                {
                    'id' : index+1,
                    'name_subject' : subject[1],
                    'code_subject' : subject[2],
                    'stc' : subject[3],
                } for index, subject in enumerate(results)] 
            return subjects    
        '''
        : return objects in array
        '''   
        return None
    def store_record_subjects(self,subject):
        user_id = DB().select_data('select id from users where username = %s',(subject.get('username'),))
        if len(user_id) > 0:
            check_record = DB().select_data('select * from record_subject_to_regis where code_subject = %s and user_id = %s',(subject.get('code_subject'),user_id[0][0]))
            if len(check_record) > 0:
                DB().update('update record_subject_to_regis set group_name = %s, team_name = %s, lop=%s, date=%s, id_to_hoc=%s where code_subject = %s and user_id = %s',
                            (
                                subject.get('group_name'),
                                subject.get('team_name'),
                                subject.get('code_subject'),
                                user_id[0][0],
                                subject.get('lop'),
                                '',
                                subject.get('id_to_hoc')
                             ))
            else:
                DB().insert_data("""insert into record_subject_to_regis
                    (code_subject, name_subject, group_name, team_name, stc, user_id, lop, date, id_to_hoc)
                    values (%s, %s, %s, %s, %s, %s,%s, %s, %s)
                    """,
                    (
                        subject.get('code_subject'),
                        subject.get('name_subject'),
                        subject.get('group_name'),
                        subject.get('team_name'),
                        subject.get('stc'),
                        user_id[0][0],
                        subject.get('lop'),
                        '',
                        subject.get('id_to_hoc')
                    )
                )
            return {
                'Message': 'Insert successfully'
            }
        else:
            return {
                'Message': 'Invalid username'
            }
    def fetchRecords(self, username):
        user_id = DB().select_data('select id from users where username = %s',(username,))
        if len(user_id) > 0:
            records = DB().select_data("select * from record_subject_to_regis where user_id = %s",(user_id[0][0],))
            # print(records)
            if len(records) > 0:
                return {
                    'Message': 'Fetch successfully',
                    'Records': [{
                        'codeSubject': record[1],
                        'nameSubject': record[2],
                        'group_name': record[3],
                        'team_name': record[4],
                        'stc': record[5],
                        'signed': record[7],
                        'lop': record[8],
                        'date': record[9],
                        'id_to_hoc': record[10]
                        
                    } for record in records]
                }
            else:
                return {
                    'Message': 'Fetch successfully',
                    'Records': None
                }
        else:
            return {
                'Message': 'Fetch failed'
            }
    def update_subject_signed(self, codeSubject, username):
        check = DB().select_data("select * from record_subject_to_regis where code_subject = %s and user_id = (select id from users where username=%s)",(codeSubject, username))
        if len(check) == 0:
            return {
                'Status': False,
                'Message': 'code_subject or username is changed at local or not found on server'
            }
        else:
            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            DB().update("update record_subject_to_regis set signed = 1, date=%s where code_subject = %s and user_id = (select id from users where username=%s)",(date, codeSubject, username))
            return {
                'Status': True,
                'Message': 'Updated singed subject'
            }
            
    def deleteOneSubjectFromRecord(self, codeSubject, username):
        signed = DB().select_data("select signed from record_subject_to_regis where code_subject=%s and user_id=(select id from users where username=%s)",(codeSubject, username))
        # print(signed)
        if len(signed) == 0:
            return {
                'Status': False,
                'Message':'Username or CodeSubject not found'
            }
        else:
            if signed[0][0] == 1:
                return {
                    'Status': False,
                    'Message': 'This subject has been successfully registered'
                }
            else:
                DB().delete("delete from record_subject_to_regis where code_subject=%s and user_id=(select id from users where username=%s)",(codeSubject,username))
                return {
                    'Status': True,
                    'Message': 'Delete successfully'
                }
    def find_name_subject(self, codeSubject):
        name = DB().select_data("select nameSubject from subjects where codeSubject=%s",(codeSubject,))
        if len(name) > 0:
            return name[0][0]
        else:
            return 'Dont worry bro! This subject not found my own server but has been already exists at QLDT'