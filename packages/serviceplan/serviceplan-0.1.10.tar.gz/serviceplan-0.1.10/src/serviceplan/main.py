import mysql.connector
import requests
from dlmail.dlmail import DlMail



class ServerPlan:
    def __init__(self, dbhost=None,dbuser=None,dbpassword=None,dbdatabase=None,sql_query=None, url=None,myproxy=None,timeout=10,smtp_host=None,password=None,sender=None,subject=None,mailto=None,cc=None):
        self.host = dbhost
        self.user = dbuser
        self.password = dbpassword
        self.database = dbdatabase
        self.myproxy = myproxy
        self.timeout = timeout

        self.smtp_host = smtp_host
        self.password = password
        self.subject = subject
        self.mailto = mailto
        self.cc = cc
        
        self.connection = mysql.connector.connect(
                host=self.host, user=self.user, password=self.password, database=self.database
            )

        if sql_query is None:
            self.sql_query = (
                "SELECT project_name_info, alias, ocserver_info, rds_info FROM wosapp_server_result "
                "WHERE switch_status = '0' AND (rds_info = 'available' OR ocserver_info = 'RUNNING')"
            )
        else:
            self.sql_query = sql_query
        if url is None:
            self.url = "https://open.feishu.cn/open-apis/bot/v2/hook/39ee"
        else:
            self.url = url


    def push_message(self, json, headers, my_proxy, timeout):
        max_retries = 0
        retries = 1
        while retries > max_retries:
            try:
                proxy_address = my_proxy.get_healthiest_proxy()
                resp = requests.post(url=self.url, json=json, headers=headers, proxies={'http': proxy_address, 'https': proxy_address},
                                timeout=timeout)
                if resp.status_code == 200:
                    my_proxy.update_proxy_health(proxy_address, 'success')
                    return resp
                else:
                    my_proxy.update_proxy_health(proxy_address, 'fail')
                    retries += 1
            except Exception as e:
                my_proxy.update_proxy_health(proxy_address, 'fail')
                retries += 1
                print(f"Request failed with error: {e}")
        return None

    def push_mail_message(self, message, headers):
        smtp_host=self.smtp_host
        password =self.password
        sender=self.sender
        subject=self.subject
        mailto=self.mailto
        cc = self.cc

        dlmail = DlMail(password=password, smtp_host=smtp_host)
        dlmail.sendhtml_dlmail(subject=subject,message=message,mailto=mailto,cc=cc)


    def serverplan(self):
        cursor = self.connection.cursor()
        cursor.execute(self.sql_query)
        results = cursor.fetchall()
        message = "服务未关闭的项目:\n"
        message2 = "服务未关闭的项目:<br>"
        i = 0
        j = 0
        for row in results:
            i = i + 1
            project_name_info, alias, ocserver_info, rds_info = row
            message += f"{i}、{project_name_info}\t\t{alias}\n"

        for row in results:
            j = j + 1
            project_name_info, alias, ocserver_info, rds_info = row
            message2 += f"{j}、{project_name_info}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{alias}</br>"
        cursor.close()
        self.connection.close()
        headers = {"Content-Type": "application/json"}
        data = {"msg_type": "text", "content": {"text": message}}
        #response = requests.post(self.url, json=data, headers=headers,proxies={'http': proxy_address, 'https': proxy_address},timeout=10)
        response = self.push_message(data,headers,self.myproxy,self.timeout)
        response2 = self.push_mail_message(message2,headers)
        return response.text

