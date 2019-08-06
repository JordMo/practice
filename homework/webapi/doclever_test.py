import unittest
import requests
import os
# from utils.HTMLTestRunner import HTMLTestRunner
from utils.HTMLTestRunner_cn import HTMLTestRunner

REPORT_DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../report')

class Constant:
    HOST = "www.doclever.cn"
    PORT = "8090"
    DOCLEVER_HOST = "http://" + HOST + ":" + PORT
    LOGIN_URL = DOCLEVER_HOST + "/user/login"
    UPDATE_URL = DOCLEVER_HOST + "/user/save"
    EDIT_PWD_URL = DOCLEVER_HOST + "/user/editpass"


class DocleverTest(unittest.TestCase):
    """Doclever 测试用例"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # cls.login()

    @staticmethod
    def login():
        params = {
            "name": "do自己",
            "password": "123456"
        }
        # res = requests.post(Constant.LOGIN_URL, params)
        #通过session进行登录
        sess=requests.session()
        res=sess.post(Constant.LOGIN_URL, params)
        print(res.json())
        print(res.cookies)
        print(res.headers)
        return res

    @staticmethod
    def login_session():
        params = {
            "name": "do自己",
            "password": "123456"
        }
        # res = requests.post(Constant.LOGIN_URL, params)
        #通过session进行登录
        sess=requests.session()
        res=sess.post(Constant.LOGIN_URL, params)
        return sess

    def cookies(self):
        res = DocleverTest.login()
        print(res.cookies)
        return res.cookies

    def test_login(self):
        """登录--正常用户名及密码"""
        res=DocleverTest.login()
        code = res.json().get("code")
        self.login_cookies=res.cookies.get("connect.sid")
        print(self.login_cookies)
        expected_res = {"code":200,"msg":"ok"}
        self.assertEqual(code, expected_res['code'], expected_res['msg'])

    def test_login_wrong(self):
        """登录--用户名或者密码错误"""
        params = {
            "name": "doclever@2019",
            "password": "12345"
        }
        res = requests.post(Constant.LOGIN_URL, params)
        code = res.json().get("code")
        expected_res = {"code": 2, "msg": "用户名或者密码错误"}
        self.assertEqual(code, expected_res['code'], expected_res['msg'])

    def test_update_age(self):
        """个人信息--更新用户AGE"""
        params = {
            "userid": "5c6cba453dce46264b263b97",
            "age": "100"
        }
        res = requests.post(Constant.UPDATE_URL, params)
        code = res.json().get("code")
        expected_res = {"code": 200, "msg": "ok"}
        self.assertEqual(code, expected_res['code'], expected_res['msg'])

    def test_update_age_exceed(self):
        """
        个人信息--更新用户AGE
        """
        params = {
            "userid": "5c6cba453dce46264b263b97",
            "age": "12345"
        }
        res = requests.post(Constant.UPDATE_URL, params)
        code = res.json().get("code")
        expected_res = {"code": 11, "msg": "参数age验证失败"}
        self.assertEqual(code, expected_res.get("code"),expected_res.get("msg"))

    def test_update_age_notnumber(self):
        """
        个人信息--更新用户AGE
        {"code":12,"msg":"参数age必须为number"}
        """
        params = {
            "userid": "5c6cba453dce46264b263b97",
            "age": "123s"
        }
        res = requests.post(Constant.UPDATE_URL, params)
        code = res.json().get("code")
        expected_res = {"code":12,"msg":"参数age必须为number"}
        self.assertEqual(code, expected_res.get("code"),expected_res.get("msg"))

    def test_edit_pwd(self):
        """个人信息--修改密码"""
        params = {
            "userid": "5c6cba453dce46264b263b97",
            "oldpass": "123456",
            "newpass":"123456"
        }
        res = requests.put(Constant.EDIT_PWD_URL, params,cookies=self.cookies())
        print(res.json())
        code = res.json().get("code")
        expected_res = {"code":200,"msg":"修改成功","data":"修改成功"}
        self.assertEqual(code, expected_res.get("code"), expected_res.get("msg"))

    def test_edit_pwd_withoutcookies(self):
        """个人信息--修改密码不用cookies请求"""
        params = {
            "userid": "5c6cba453dce46264b263b97",
            "oldpass": "123456",
            "newpass":"123456"
        }
        res = self.login_session().put(Constant.EDIT_PWD_URL, params)
        print(res.json())
        code = res.json().get("code")
        expected_res = {"code":200,"msg":"修改成功","data":"修改成功"}
        self.assertEqual(code, expected_res.get("code"), expected_res.get("msg"))


if __name__ == '__main__':
    # unittest.main(verbosity=2)
    testcase = unittest.TestLoader().loadTestsFromTestCase(DocleverTest)
    suite= unittest.TestSuite()
    suite.addTest(testcase)
    report = os.path.join(REPORT_DIR, 'report.html')
    print(report)
    with open(report, 'wb+') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='Doclever WEB API TEST', description='Doclever WEB API TEST RESULT')
        runner.run(suite)
    f.close()


