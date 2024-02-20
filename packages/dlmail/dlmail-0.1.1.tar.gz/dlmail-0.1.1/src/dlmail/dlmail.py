import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import re
import os

def embed_images_in_html(html_content, base_dir):
    # 正则表达式匹配图片标签
    img_regex = r'<img\s+src="([^"]+)"\s*'

    def img_to_base64(match):
        # 获取图片路径
        img_path = match.group(1)
        # 如果图片路径是相对路径，则转换为绝对路径
        if not img_path.startswith('http://') and not img_path.startswith('https://'):
            img_path = os.path.join(base_dir, img_path.lstrip('/'))
            print(img_path)
        # 读取图片文件并转换为 base64 编码
        with open(img_path, 'rb') as f:
            img_data = f.read()
            img_base64 = base64.b64encode(img_data).decode('utf-8')
            print(img_base64)
        # 构建替换后的图片标签
        return f'<img src="data:image/png;base64,{img_base64}"'

    # 使用正则表达式替换图片标签
    html_content_with_base64 = re.sub(img_regex, img_to_base64, html_content)
    return html_content_with_base64


class DlMail:
    def __init__(self, smtp_host=None, smtp_port=587, user='dong.lin', password='111111', sender='dong.lin@test.com', starttls=True):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.user = user
        self.password = password
        self.sender = sender
        self.starttls = starttls


    def sendhtml_dlmail(self,subject,message,mailto,cc):
        base_dir = '/home/ops/tmp/dlmail/src/dlmail'
        html_with_base64 = embed_images_in_html(message, base_dir)
        message=html_with_base64
        smtp = smtplib.SMTP(self.smtp_host, self.smtp_port)
        if self.starttls:
            smtp.starttls()
        smtp.login(self.user, self.password)
        print('已登录邮箱')
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = ";".join(mailto)
        msg['Cc'] = ";".join(cc)
        msg.attach(MIMEText(message, 'html'))
        receiver = mailto + cc
        smtp.sendmail(self.sender,receiver, msg.as_string())  # 发送邮件，这里的msg.as_string是邮件的正文部分


    def test(self):
        print(self.smtp_host)


