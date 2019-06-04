from Common import Request, Assert

request = Request.Request()
assertion = Assert.Assertions()
url = 'http://192.168.1.137:8080/'

class Login():
    def get_token(self):
        login_resp = request.post_request(url=url+'admin/login',
                                            json={"username": "admin", "password": "123456"})

        resp_dict = login_resp.json()
        assertion.assert_code(login_resp.status_code,200)
        assertion.assert_in_text(resp_dict['message'],'成功')

        data_dict = resp_dict['data']
        token = data_dict['token']
        tokenHead = data_dict['tokenHead']
        head ={ 'Authorization' : tokenHead+token}
        return head

