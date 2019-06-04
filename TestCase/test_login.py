#调用第三方模块
import allure
import pytest
from Common import Request,Assert,read_excel
#给类实例化
request = Request.Request()

assertions = Assert.Assertions()

excel_list = read_excel.read_excel_list('./document/test.xlsx')
ids_list = []
for i in range(len(excel_list)):
    # 删除excel_list中每个小list的最后一个元素,并赋值给ids_pop
    ids_pop = excel_list[i].pop()
    # 将ids_pop添加到 ids_list 里面
    ids_list.append(ids_pop)


@allure.feature('登录模块')
class Test_login:

    @allure.story('登录')
    def test_login(self):

        # request.post_request 发送一个post请求 ( 传入参数 ) , 将响应结果返回赋值 给 login_resp
        login_resp = request.post_request(url='http://192.168.60.132:8080/admin/login',
                                            json={"username": "admin", "password": "123456"})
        # 响应状态码 :login_resp.status_code
        # 调用断言数字的方法: assertions.assert_code
        assertions.assert_code(login_resp.status_code,200)

        # login_resp.text : 获取 响应正文 (字符串格式)
        print(login_resp.text)
        print(type(login_resp.text))
        # login_resp.json() : 获取 响应正文 (字典格式)
        login_resp_json = login_resp.json()
        print(type(login_resp_json))

        # 调用断言字符包含的方法: assertions.assert_in_text
        assertions.assert_in_text(login_resp_json['message'],'成功')

    @allure.story('登录参数化')
    @pytest.mark.parametrize('name,pwd,msg',excel_list,ids=ids_list)
    def test_login1(self,name,pwd,msg):
        # request.post_request 发送一个post请求 ( 传入参数 ) , 将响应结果返回赋值 给 login_resp
        login_resp = request.post_request(url='http://192.168.60.132:8080/admin/login',
                                          json={"username": name, "password": pwd})
        # 响应状态码 :login_resp.status_code
        # 调用断言数字的方法: assertions.assert_code
        assertions.assert_code(login_resp.status_code, 200)

        # login_resp.text : 获取 响应正文 (字符串格式)
        print(login_resp.text)
        print(type(login_resp.text))
        # login_resp.json() : 获取 响应正文 (字典格式)
        login_resp_json = login_resp.json()
        print(type(login_resp_json))

        # 调用断言字符包含的方法: assertions.assert_in_text
        assertions.assert_in_text(login_resp_json['message'], msg)


