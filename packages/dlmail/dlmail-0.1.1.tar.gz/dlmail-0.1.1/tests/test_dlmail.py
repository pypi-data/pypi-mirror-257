from dlmail.dlmail import DlMail
import unittest


class TestDlMail(unittest.TestCase):
    def test_sendhtml_dlmail(self):

        # 编写测试用例
        message="<a>123</a></br><a>345</a>"
        smtp_host='smtp.neusoft.com'
        password ='Aa120310772'
        sender='dong.lin@neusoft.com'
        subject='test subject'
        mailto=['dong.lin@neusoft.com']
        cc = ['dong.lin@neusoft.com']


        dlmail = DlMail(password=password, smtp_host=smtp_host)
        dlmail.sendhtml_dlmail(subject=subject,message=message,mailto=mailto,cc=cc)


        return 

if __name__ == '__main__':
    unittest.main()
