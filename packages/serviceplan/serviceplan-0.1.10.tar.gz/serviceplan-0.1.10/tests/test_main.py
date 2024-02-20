from serviceplan.main import ServerPlan
import myproxy
import unittest

class TestServerPlan(unittest.TestCase):
    def test_serverplan(self):
        proxies = [
            {'address': 'http://10.10.90.75:1005', 'health': 10},
            {'address': 'http://10.10.90.75:1006', 'health': 0}
        ]
        my_proxy = myproxy.Config(proxies)

        # 编写测试用例
        host='10.10.90.75'
        user='root'
        password='LY_18840648500'
        database='wosys'

        sql_query = ("SELECT project_name_info, alias, ocserver_info, rds_info FROM wosapp_server_result "
                     "WHERE switch_status = '0' AND (rds_info = 'available' OR ocserver_info = 'RUNNING')")

        url = "https://open.feishu.cn/open-apis/bot/v2/hook/39ee35a7-99af-468c-9e70-04d497cce82b"

        serverplan = ServerPlan(host, user, password, database, sql_query, url,my_proxy)

        res = serverplan.serverplan()

        return res

if __name__ == '__main__':
    unittest.main()
