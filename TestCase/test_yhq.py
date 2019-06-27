import allure
import pytest
from Common import Request,Assert,read_excel

request = Request.Request()

assertions = Assert.Assertions()

head = {}
yhq_id = 0
excel_list = read_excel.read_excel_list('./document/优惠券.xlsx')
ids_list = []
for i in range(len(excel_list)):
    # 删除excel_list中每个小list的最后一个元素,并赋值给ids_pop
    ids_pop = excel_list[i].pop()
    # 将ids_pop添加到 ids_list 里面
    ids_list.append(ids_pop)


@allure.feature("优惠券模块")
class Test_yhq:

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

    @allure.story("查询优惠券")
    def test_sel(self):
        login_resp = request.get_request(url='http://192.168.60.132:8080/coupon/list',
                                         params={'pageNum':1,'pageSize':10}, headers=head)
        assertions.assert_code(login_resp.status_code, 200)
        login_resp_json = login_resp.json()
        assertions.assert_in_text(login_resp_json['message'], '成功')

        resp_data = login_resp_json['data']
        data_list = resp_data['list']
        yhq_dict = data_list[0]
        global yhq_id
        yhq_id = yhq_dict['id']

    @allure.story("删除优惠券")
    def test_del(self):
        login_resp = request.post_request(url='http://192.168.60.132:8080/coupon/delete/'+str(yhq_id),
                                          headers=head)
        assertions.assert_code(login_resp.status_code, 200)
        login_resp_json = login_resp.json()
        assertions.assert_in_text(login_resp_json['message'], '成功')

    @allure.story("添加优惠券")
    def test_add(self):
        login_resp = request.post_request(url='http://192.168.60.132:8080/coupon/create',
                                          json={"type":0,"name":"节日大促","platform":0,
                                                "amount":20,"perLimit":1,"minPoint":50,
                                                "startTime":"","endTime":"","useType":0,
                                                "note":"","publishCount":1000,"productRelationList":[],
                                                "productCategoryRelationList":[]},headers=head)
        assertions.assert_code(login_resp.status_code, 200)
        login_resp_json = login_resp.json()
        assertions.assert_in_text(login_resp_json['message'], '成功')

    @allure.story("添加优惠券_参数化")
    @pytest.mark.parametrize('name,amount,minPoint,publishCount,msg',excel_list,ids=ids_list)
    def test_add(self,name,amount,minPoint,publishCount,msg):
        login_resp = request.post_request(url='http://192.168.60.132:8080/coupon/create',
                                          json={"type":0,"name":name,"platform":0,
                                                "amount":amount,"perLimit":1,"minPoint":minPoint,
                                                "startTime":"null","endTime":"null","useType":0,
                                                "note":"null","publishCount":publishCount,"productRelationList":[],
                                                "productCategoryRelationList":[]},headers=head)
        assertions.assert_code(login_resp.status_code, 200)
        login_resp_json = login_resp.json()
        assertions.assert_in_text(login_resp_json['message'], msg)