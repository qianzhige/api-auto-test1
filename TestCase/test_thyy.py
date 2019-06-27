import allure
import pytest
from Common import Request,Assert,read_excel,Login

request = Request.Request()
assertions = Assert.Assertions()

url = Login.url
head = Login.Login().get_token()
th_id = 0
excel_list = read_excel.read_excel_list('./document/退货.xlsx')
ids_list = []
for i in range(len(excel_list)):
    # 删除excel_list中每个小list的最后一个元素,并赋值给ids_pop
    ids_pop = excel_list[i].pop()
    # 将ids_pop添加到 ids_list 里面
    ids_list.append(ids_pop)

@allure.feature("退货模块")
class Test_th:

    @allure.story("查询退货")
    def test_sel(self):
        sel_resp = request.get_request(url=url+'returnReason/list',
                                         params={'pageNum':1,'pageSize':5}, headers=head)
        assertions.assert_code(sel_resp.status_code, 200)
        sel_resp_json = sel_resp.json()
        assertions.assert_in_text(sel_resp_json['message'], '成功')

        resp_data = sel_resp_json['data']
        data_list = resp_data['list']
        th_dict = data_list[0]
        global th_id
        th_id = th_dict['id']

    @allure.story("删除退货原因")
    def test_del(self):
        thyy_del_resp = request.post_request(url=url + 'returnReason/delete', params={'ids': th_id}, headers=head)
        assertions.assert_code(thyy_del_resp.status_code, 200)
        resp_json = thyy_del_resp.json()
        assertions.assert_in_text(resp_json['message'], '成功')

    @allure.story("添加退货")
    @pytest.mark.parametrize('name,sort,status,msg',excel_list,ids=ids_list)
    def test_add(self,name,sort,status,msg):
        add_resp = request.post_request(url=url+'returnReason/create',
                                        json={"name":name,"sort":sort,"status":status,"createTime":""},
                                        headers=head)
        assertions.assert_code(add_resp.status_code, 200)
        add_resp_json = add_resp.json()
        assertions.assert_in_text(add_resp_json['message'], msg)





