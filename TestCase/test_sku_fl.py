import allure
import pytest
from Common import Request,Assert,read_excel

request = Request.Request()

assertions = Assert.Assertions()

head = {}
fl_id = 0


@allure.feature("商品分类模块")
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
        head = {'Authorization' : token}

    @allure.story("获取分类列表")
    def test_sel(self):
        login_resp = request.get_request(url='http://192.168.60.132:8080/productCategory/list/0',
                                         params={'pageNum':1,'pageSize':5}, headers=head)
        assertions.assert_code(login_resp.status_code, 200)
        login_resp_json = login_resp.json()
        assertions.assert_in_text(login_resp_json['message'], '成功')

        resp_data = login_resp_json['data']
        data_list = resp_data['list']
        fl_dict = data_list[0]
        global fl_id
        fl_id = fl_dict['id']

    @allure.story("删除商品分类")
    def test_del(self):
        login_resp = request.post_request(url='http://192.168.60.132:8080/productCategory/delete/' + str(fl_id),
                                          headers=head)
        assertions.assert_code(login_resp.status_code, 200)
        login_resp_json = login_resp.json()
        assertions.assert_in_text(login_resp_json['message'], '成功')
    @allure.story("添加商品分类")
    def test_add(self):
        login_resp = request.post_request(url='http://192.168.60.132:8080/productCategory/create',
                                          json={"description": "", "icon": "", "keywords": "", "name": "电话的",
                                                "navStatus": 0, "parentId": 0, "productUnit": "", "showStatus": 0,
                                                "sort": 0,"productAttributeIdList": []},headers=head)
        assertions.assert_code(login_resp.status_code, 200)
        login_resp_json = login_resp.json()
        assertions.assert_in_text(login_resp_json['message'], '成功')