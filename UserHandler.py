### 用于新建一个学生和建新的clip
import requests
from bs4 import BeautifulSoup
import json
class UserHandler:

    loginUrl = "http://127.0.0.1:8000/admin/login/?next=/admin/auth/user/add/"
    addUserUrl = "http://127.0.0.1:8000/admin/auth/user/add/"
    def createStudent(self, username, password):
        s = requests.Session()
        r = s.get(self.loginUrl)
        soup = BeautifulSoup(r.text,"lxml")
        csrfmiddlewaretoken1 = soup.find_all(attrs={"name": "csrfmiddlewaretoken"})[0]
        set_cookies = r.headers['Set-cookie']       
        cookies = dict(csrftoken=set_cookies.split(';')[0].split("=")[1])
        data = {
            "username": "heyunfan",
            "password": "2Gezhuoqing",
            "next": "/admin/auth/user/add/",
            "csrfmiddlewaretoken": csrfmiddlewaretoken1.attrs["value"]
        }
        addPage = s.post(self.loginUrl,data=data)
        # set_cookies = addPage.headers['Set-cookie']
        # cookies = dict(csrftoken=set_cookies.split(';')[0].split("=")[1])
        # print(b.status_code)
        # print(addPage.status_code)
        soup2 = BeautifulSoup(addPage.text,"lxml")
        csrfmiddlewaretoken2 = soup2.find_all(attrs={"name": "csrfmiddlewaretoken"})[0]
        data ={
            "csrfmiddlewaretoken":csrfmiddlewaretoken2.attrs["value"],
            "password1": password,
            "password2": password,
            "username": username,
            "_save": "保存"
        }
        b = s.post(self.addUserUrl,data=data)
        if b.status_code==200:
            print("success")
            return True
        else:
            print("failure")
            return False
        # print(csrfmiddlewaretoken2.attrs["value"],b.status_code)

    def createClip(self,username,password,clip_outer_id,tested):
        clipUrl = "http://127.0.0.1:8000/api/clips/"
        import base64
        Authorization = username + ':' + password
        Authorization = Authorization.encode('utf-8')
        Authorization = base64.b64encode(Authorization)
        
        headers = {
            "Authorization": "Basic "+ Authorization.decode('utf-8')
        }
        data ={
            "clip_outer_id": clip_outer_id,
            "tested": tested
        }
        res = requests.post(clipUrl,headers=headers,data=data)
        result = json.loads(res.text)
        return result['id']


# a = UserHandler()
# a.createStudent("xueyu","wasd123456")
# a.createClip('wangliying','wasd180510','徐海鹏的第三次测试','2018-05-29T17:18')