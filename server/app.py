from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import config, datetime, json
import jwt, requests
from flask_mysqldb import MySQL
import models
from access_qldt import AccessQLDT

app = Flask(__name__)

mysql = MySQL(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DATABASE_NAME

CORS(app, resources={r"/*": {"origins": "*"}})


def generate_jwt_token(isLogged,username,role):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=24),
            'iat': datetime.datetime.utcnow(),
            'logged': isLogged,
            'username' : username,
            'role': role
        }
        token = jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
        return token
    except Exception as e:
        return e
def required_token(request_headers):
    token = None
    if "Authorization" in request_headers:
        token = request_headers["Authorization"].split(" ")[1]
    if not token:
        return {
            "message": "Authentication Token is missing!",
            "logged": False,
            "data": None,
            "error": "Unauthorized"
        }, 401
    try:
        data=jwt.decode(token.encode(), app.config.get('SECRET_KEY'), algorithms=["HS256"])
        # print('decode: ', data)
        if data is None or data.get('logged') != True:
            return {
            "message": "Invalid Authentication token!",
            "logged": False,
            "data": None,
            "error": "Unauthorized"
        }, 401
        return data, 200    
    except Exception as e:
        return {
            "message": "Something went wrong",
            "logged": False,
            "data": None,
            "error": str(e)
        }, 500

def get_tkb(token):
        url = config.host_qldt + "/api/sch/w-locdstkbtuanusertheohocky"
        headers = {
            'Authorization' : 'Bearer ' + token,
            'Content-Type'  : 'application/json'
        }
        data = {"filter":{"hoc_ky":20231,"ten_hoc_ky":""},"additional":{"paging":{"limit":100,"page":1},"ordering":[{"name":None,"order_type":None}]}}
        res = requests.post(url, headers=headers, json=data)
        return json.loads(res.content.decode("utf-8"))

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        # print(data)
        username = data.get('username')
        password = data.get('password').encode()
        user_already_exists = models.User().check_user_already_exists(username=username, password=password) 
        role_name = user_already_exists.get('result')[5]
        print(user_already_exists)
        if user_already_exists.get('status') == True:
            isOnline = user_already_exists.get('result')[7]
            if isOnline == 0:
                jwt_token = generate_jwt_token(isLogged=True, username=username, role=role_name)
                models.User().updateIsOnline(username=username,isOnline=1)
                # print(jwt_token)
                return {
                    'Logged':True,
                    'Access-Token' : jwt_token,
                    'Username' : username,
                    'RoleName' : role_name,
                    'Message' : 'Login successfully'
                }
            else:
                return {
                    'Logged':False,
                    'Message': 'Tài khoản được đăng nhập ở 1 nơi khác'
                }
        else:
            return {
                'Logged': False,
                'Message': 'Invalid username or password'
                }
    except Exception as e:
        # print(e)
        return {
                'Logged': False,
                'Message': 'Something went wrong'
            }

@app.route('/api/logout', methods=['POST'])
def logout():
    username = request.get_json().get('username')
    models.User().updateIsOnline(username=username,isOnline=0)
    return {
        'Status': True
    }
    
@app.route('/api/auth/authRequired', methods=['POST'])
def authRequired():
    request_headers = request.headers
    mess_token = required_token(request_headers=request_headers)
    return {
        'mess_token': mess_token
    }
@app.route('/api/isAdmin', methods=['POST'])
def isAdmin():
    headers = request.headers
    check_token = required_token(headers)
    if check_token[1] == 200:
        role = check_token[0].get('role')
        if role == 1: #is admin
            return {
                'isAdmin': True
            }
        else:
            return {
                'isAdmin': False
            }
    else:
        return check_token[0]
@app.route('/api/majors', methods=['POST'])
def get_majors():
    majors = models.Majors().get_majors_title()
    return majors

@app.route('/api/subjects', methods=['POST'])
def get_subjects_depend_major():
    major = request.get_json().get('major')
    subjects = models.Majors().get_subjects_depend_major(major=major)
    return {
        'subjects': subjects
    }
@app.route('/api/checkAccessQldt', methods=['POST'])
def check_Access_Qldt():
    data = request.get_json()
    print(data)
    usernameInCurrentApp = data.get('Username')
    msv = data.get('msv')
    password = data.get('password')
    new_user = AccessQLDT(username=msv, password=password)
    response = new_user.login()
    # print(response)
    if response.get('code') == '200':
        models.User().update_account_qldt(usernameInCurrentApp,msv,password)
    return response


@app.route('/api/submit_subject_to_qldt', methods=['POST'])
def submit_subject_to_qldt():
    data = request.get_json()
    # print(data)
    Username = data.get('Username')
    codeSubject = data.get('codeSubject')
    headers = request.headers
    # check_token = required_token(headers)
    # if check_token[1] == 200:
    if 1 == 1:
        if data.get('access_token_qldt') is not None:
            access_token_qldt = data.get('access_token_qldt')
            id_to_hoc = data.get('id_to_hoc')
            access = AccessQLDT(access_token=access_token_qldt)
            response = access.register_tkb(id_to_hoc)
            if response.get('code') == 200:
                data = response.get('data')
                is_thanh_cong = data.get('is_thanh_cong')
                if is_thanh_cong == True:
                    # dang ky thanh cong !!!
                    res = models.Majors().update_subject_signed(codeSubject,Username)
                    if res.get('Status') == True:
                        return {
                            'Message': 'Submit success !!!',
                            'Status': True
                        }
                    else:
                        return res
                else:
                    return {
                        'Message': data.get('thong_bao_loi'),
                        'Status': False
                    }
            else:
                return{
                    'Message': 'Token invalid, reload page(F5) and try login qldt again',
                    'Status': False
                }
        else:    
            return {
                'Message': 'Missing access_token_qldt, you need try login qldt again',
                'Status': False
            }
    else:
        return {
            'Message' : 'Invalid token in current app, you need try login current app again',
            'Logged': False,
        }

@app.route('/api/findSubjectWithCode', methods=['POST'])
def findSubjectWithCode():
    data = request.get_json()
    # print(data.get('codeSubject'))
    codeSubject = data.get('codeSubject').strip()
    group_name = data.get('group_name').strip()
    team_name = data.get('team_name').strip()
    subject = models.Majors().findSubjectWithCode(codeSubject,group_name,team_name)
    nameSubject = models.Majors().find_name_subject(codeSubject)
    if subject is not None:
        return {
            'Message': 'Found',
            'nameSubject': nameSubject,
            'codeSubject': subject[1],
            'id_to_hoc': subject[2],
            'group_name': subject[4],
            'team_name': subject[5],
            'stc': subject[6],
            'lop': subject[7]
            
        }
    else:
        return {
            'Message': 'Not found'
        }
@app.route('/api/storeSubject', methods=['POST'])
def storeSubject():
    data = request.get_json()
    # print(data)
    res = models.Majors().store_record_subjects(data)
    return res

@app.route('/api/fetchRecords', methods=['POST'])
def fetchRecords():
    data = request.get_json()
    username = data.get('username')
    if username is not None:
        res = models.Majors().fetchRecords(username)
    else:
        res = []
    return res

@app.route('/api/CheckExpressTokenQLDT', methods=['POST'])
def checkExpressTokenQLDT():
    data = request.get_json()
    AccessTokenQLDT = data.get('AccessTokenQLDT')
    # print(AccessTokenQLDT)
    host = "https://qldt.ptit.edu.vn/api/dkmh/w-checkvaliddangkymonhoc"
    headers = {
        "Authorization": "Bearer " + AccessTokenQLDT,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        }
    res = requests.post(host, headers=headers, allow_redirects=False)
    return json.loads(res.content.decode('utf-8'))
@app.route('/api/deleteOneSubjectFromRecord', methods=['POST'])
def deleteOneSubjectFromRecord():
    data = request.get_json()
    username = data.get('username')
    codeSubject = data.get('codeSubject')
    res = models.Majors().deleteOneSubjectFromRecord(codeSubject,username)
    return res

@app.route('/api/fetch_users_jsdgfjsa23u4', methods=['POST'])
def fetch_users_jsdgfjsa23u4():
    headers = request.headers
    check_token = required_token(headers)
    if check_token[1] == 200:
        role = check_token[0].get('role')
        if role == 1: #is admin
            users = models.User().FetchALlUsers()
            return {
                'lists': users,
                'isAdmin': True
            }
        else:
            return {
                'lists': None,
                'isAdmin': False
            }
    else:
        return check_token[0]
@app.route('/api/create_users_jsdgfjsa23u4', methods=['POST'])
def create_users_jsdgfjsa23u4():
    headers = request.headers
    check_token = required_token(headers)
    if check_token[1] == 200:
        role = check_token[0].get('role')
        if role == 1: #is admin
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            res = models.User().CreateUser(username,password)
            return res
        else:
            return {
                'result': False,
                'Message': 'you are not administrator',
                'isAdmin': False
            }
    else:
        return check_token[0]

if __name__ == '__main__':
    app.run(debug=True)