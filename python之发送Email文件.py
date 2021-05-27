import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import random


class SendEMail(object):
    """封装发送邮件类"""

    def __init__(self):
        self.host = "smtp.qq.com"
        self.port = 465
        self.msg_from = "1850555135@qq.com"
        self.password = "npleqjqdtuyjigfj"     # qq邮箱 授权码 npleqjqdtuyjigfj

        # 邮箱服务器地址和端口
        self.smtp_s = smtplib.SMTP_SSL(host= self.host, port=self.port)

        # 发送方邮箱账号和授权码
        self.smtp_s.login(user=self.msg_from, password=self.password)

    def send_text(self, to_user, subject, content):
        """
        发送文本邮件
        :param to_user: 对方邮箱
        :param content: 邮件正文
        :param subject: 邮件主题
        :param content_type: 内容格式：'plain' or 'html'
        :return:
        """
        msg = MIMEText(content, _subtype='html', _charset="utf8")

        msg["From"] = format_addr("菜鸟测试<{0}>".format(self.msg_from))
        msg["To"] = to_user
        msg["subject"] = subject

        self.smtp_s.send_message(msg, from_addr=self.msg_from, to_addrs=to_user)

    def send_file(self, to_user, content, subject, reports_path, filename, content_type='plain'):
        """
        发送带文件的邮件
        :param to_user: 对方邮箱
        :param content: 邮件正文
        :param subject: 邮件主题
        :param reports_path: 文件路径
        :param filename: 邮件中显示的文件名称
        :param content_type: 内容格式
        """

        file_content = open(reports_path, "rb").read()

        msg = MIMEMultipart()

        text_msg = MIMEText(content, _subtype=content_type, _charset="utf8")
        msg.attach(text_msg)

        file_msg = MIMEApplication(file_content)
        file_msg.add_header('content-disposition', 'attachment', filename=filename)
        msg.attach(file_msg)

        msg["From"] = self.msg_from
        msg["To"] = to_user
        msg["subject"] = subject

        self.smtp_s.send_message(msg, from_addr=self.msg_from, to_addrs=to_user)

    def send_img(self, to_user, subject, content, filename, content_type='html'):
        '''
        发送带图片的邮件
        :param to_user: 对方邮箱
        :param subject: 邮件主题
        :param content: 邮件正文
        :param filename: 图片路径
        :param content_type: 内容格式
        '''
        subject = subject
        msg = MIMEMultipart('related')
        # Html正文必须包含<img src="cid:imageid" alt="imageid" width="100%" height="100%>
        content = MIMEText(content, _subtype=content_type, _charset="utf8")
        msg.attach(content)
        msg['Subject'] = subject
        msg['From'] = self.msg_from
        msg['To'] = to_user

        with open(filename, "rb") as file:
            img_data = file.read()

        img = MIMEImage(img_data)
        img.add_header('Content-ID', 'imageid')
        msg.attach(img)

        self.smtp_s.sendmail(self.msg_from, to_user, msg.as_string())


def format_addr(SendUser):
    """
    格式化发送人
    :param SendUser 发件人
    """
    name, addr = parseaddr(SendUser)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def CodeText(ToUser, Code):
    """
    验证码文本
    ：param ToUser 发送人
    :param Code 要发送的随机验证码
    """
    txt = """
     <div class="mmsgLetter" style="width:580px;margin:0 auto;padding:10px;color:#333;background-color:#fff;border:0px solid #aaa;border-radius:5px;-webkit-box-shadow:3px 3px 10px #999;-moz-box-shadow:3px 3px 10px #999;box-shadow:3px 3px 10px #999;font-family:Verdana, sans-serif; ">
        <div class="mmsgLetterHeader" style="height:23px;">
        </div>
        <div class="mmsgLetterContent" style="text-align:left;padding:30px;font-size:14px;line-height:1.5;">
            <div>
                <p class="salutation" style="font-weight:bold;">
                    Hi,<span id="mailUserName">{0}</span>：
                </p>
                <strong style="display:block;margin-bottom:15px;">
                    您本次获取的验证码为：<span style="color:#f60;font-size: 24px">{1}</span>
                </strong>
                <div style="margin-bottom:30px;">
                    <small style="display:block;margin-bottom:20px;font-size:12px;">
                        <p style="color:#747474;">
                            注意：此操作可能会修改您的密码、登录邮箱或绑定手机。如非本人操作，请及时登录并修改密码以保证帐户安全
                            <br>(工作人员不会向你索取此验证码，请勿泄漏！)
                        </p>
                    </small>

                    <div style="padding:10px 10px 0;border-top:1px solid #ccc;color:#747474;margin-bottom:20px;line-height:1.3em;font-size:12px;">
                        <p>此为系统邮件，请勿回复<br>
                            请保管好您的邮箱，避免账号被他人盗用
                        </p>
                        <p>本次用于账号测试学习</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """.format(ToUser, Code)
    return txt

def GetRandomCode():
    num = [str(random.randint(1,9)) for qs in range(6)]
    code = "".join(num)
    return code

# if __name__ == '__main__':
#     ToUser = "zhuhuachao_0314hua@163.com"
#     email = SendEMail()
#     subject = "菜鸟测试验证码"
#     email.send_text(ToUser, subject, CodeText(ToUser,GetRandomCode()))
#     print("已发送")
