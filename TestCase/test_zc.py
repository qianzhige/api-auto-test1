import allure
import pytest
from Common import Request,Assert,read_excel,Login,Tools

request = Request.Request()
assertions = Assert.Assertions()
num = Tools.phone_num()


excel_list = read_excel.read_excel_list('../document/用户注册.xlsx')
ids_list = []

for i in range(len(excel_list)):
    ids_pop = excel_list[i].pop()
    ids_list.append(ids_pop)

@allure.feature("用户注册模块")
class Test_yhzc:

    @allure.story("注册")
    @pytest.mark.parametrize('phone,pwd,rePwd,userName,code',excel_list,ids=ids_list)
    def test_yhzc(self,phone,pwd,rePwd,userName,code):
        yhzc_resp = request.post_request(url='http://192.168.60.132:1811/user/signup',
                                            json={"phone": Tools.phone_num(), "pwd":'a123456', "rePwd":'a123456', "userName": Tools.random_str_abc(3)+Tools.random_123(3)})
        assertions.assert_code(yhzc_resp.status_code, 200)
        yhzc_resp_json = yhzc_resp.json()
        assertions.assert_in_text(yhzc_resp_json['respCode'],code)