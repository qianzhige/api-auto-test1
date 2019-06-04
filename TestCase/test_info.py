import allure
import pytest
from Common import Request,Assert,read_excel

request = Request.Request()

assertions = Assert.Assertions()

head = {}

@allure.feature("获取用户信息")
class Test_info:

    @allure.story("登录接口")
    def test_login(self):
        login_resp = request.post_request(url='http://192.168.60.132:8080/admin/login',
                                          json={"username": "admin", "password": "123456"})
        assertions.assert_code(login_resp.status_code, 200)
        login_resp_json = login_resp.json()
        assertions.assert_in_text(login_resp_json['message'], '成功')

        # 提取token
        data_json = login_resp_json['data']
        token = data_json['tokenHead'] + data_json['token']
        print(token)

        # 重新赋值全局变量 head
        global head
        head = {'Authorization' : token }

    @allure.story("用户信息接口")
    def test_info(self):
        info_resp = request.get_request(url='http://192.168.60.132:8080/admin/info', headers=head)
        assertions.assert_code(info_resp.status_code, 200)
        info_resp_json = info_resp.json()
        assertions.assert_in_text(info_resp_json['message'], '成功')

    @allure.story("获取商品列表")
    def test_sku(self):
        sku_resp = request.get_request(url='http://192.168.60.132:8080/product/list',
                                          params={'pageNum': 1, 'pageSize': 5}, headers=head)

        assertions.assert_code(sku_resp.status_code, 200)
        sku_resp_json = sku_resp.json()
        assertions.assert_in_text(sku_resp_json['message'], '成功')

