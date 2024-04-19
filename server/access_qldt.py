import requests, json

class AccessQLDT:

    def __init__(self,access_token=None, username=None, password=None):
        
        self.host = "https://qldt.ptit.edu.vn"
        self.username, self.password = username, password
        self.token = access_token
        self.cookies = None
        self.session = requests.Session()
    
    def get_cookie(self):
        path = "/api/web/w-locdssettingdangnhap"
        headers = {
            'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
            'Content-Type' : 'application/json',
            'Content-Length'  : "0",
            'Connection' : 'close',
        }
        res = self.session.post(self.host+path,headers=headers,allow_redirects=False)
        self.cookies = res.headers['Set-Cookie']
        
    def login(self):
        data_str = f"username={self.username}&password={self.password}&grant_type=password"
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
            'Content-Length' : str(len(data_str))
        }
        res = self.session.post(self.host+"/api/auth/login",headers=headers,data=data_str,allow_redirects=False)
        '''
        : return 200 is login successful
        : 403 is not authorized
        '''
        if res.status_code == 200:
            self.token = json.loads(res.content.decode('utf-8')).get('access_token').strip()
            return json.loads(res.content.decode("utf-8"))
        else:
            return json.loads(res.content.decode("utf-8"))
            
    
    def loc_ds_nhom_to(self):
        uri = "/api/dkmh/w-locdsnhomto"
        print('token: ',self.token)
        headers = {
            "Authorization": 'Bearer ' + self.token,
            'Content-Type'  : 'application/json'
        }
        data = {"is_CVHT":'false',"additional":{"paging":{"limit":8000,"page":1},"ordering":[{"name":"","order_type":""}]}}
        res  = requests.post(self.host + uri, headers=headers, json=data)
        return json.loads(res.content.decode("utf-8"))
    
    def get_tkb(self):
        uri = "/api/sch/w-locdstkbtuanusertheohocky"
        headers = {
            'Authorization' : 'Bearer ' + self.token,
            'Content-Type'  : 'application/json'
        }
        data = {"filter":{"hoc_ky":20231,"ten_hoc_ky":""},"additional":{"paging":{"limit":100,"page":1},"ordering":[{"name":None,"order_type":None}]}}
        res = self.session.post(self.host + uri, headers=headers, json=data)
        print(self.session.cookies.get_dict())
        print(res.content.decode("utf-8"))
        print(self.token)
    
    def register_tkb(self, id_to_hoc):
        uri = '/api/dkmh/w-xulydkmhsinhvien'
        headers = {
            'Authorization' : 'Bearer ' + self.token,
            'Content-Type'  : 'application/json'
        }
        proxies = {
            'http': 'http://localhost:8080'
        }
        data={"filter": {"id_to_hoc": id_to_hoc, "is_checked": True, "sv_nganh": 10}}
        res = requests.post(self.host + uri, headers=headers, json=data,allow_redirects=False)
        print(res.text)
        return json.loads(res.content.decode("utf-8"))
        

# new_user = User("b21dctm016","12092003")
# new_user.get_cookie()
# new_user.login()
# new_user.get_tkb()