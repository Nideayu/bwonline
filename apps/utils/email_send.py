from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyecord
from bwonline.settings import EMAIL_FROM


# 生成随机字符串
def random_str(random_length=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0,length)]
    return str


# 发送注册邮件
def send_register_eamil(email, send_type='register'):
    # 发送之前先保存到数据库，到时候查询链接是否存在
    # 实列化一个EmailVerifyRecord对象
    email_record = EmailVerifyecord()
    # 生成随机的code放入链接
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_record.save()
    # 定义邮件内容
    email_title = ''
    email_body = ''
    if send_type == 'register':
        email_title = '阿钰注册激活链接'
        email_body = '请点击下面激活你的账号： http://127.0.0.1:8000/active/{0}'.format(code)
        # 使用django内置函数完成邮件发送。四个参数：主题，邮件内容，发送地址，收件人（是一个字符串列表）
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        # 如果发送成功
        if send_status:
            pass
    if send_type == 'forget':
        email_title = '阿钰找回密码'
        email_body = '请点击下面的链接找回你的密码: http://127.0.0.1:8000/reset/{0}"'.format(code)
        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 如果发送成功
        if send_status:
            pass
# 前面四个参数必须要，后面的参数可以为空
#
# 发送电子邮件的最简单方法是使用 django.core.mail.send_mail()。
#
# 的subject，message，from_email和recipient_list参数是必需的。
#
#     subject：一个字符串。
#     message：一个字符串。
#     from_email：一个字符串。
#     recipient_list：字符串列表，每个字符串都是电子邮件地址。每个成员都recipient_list将在电子邮件的“收件人：”字段中看到其他收件人。
#     fail_silently：一个布尔值。如果是的话False，send_mail会提出一个smtplib.SMTPException。有关smtplib可能的例外列表，请参阅文档，所有这些例外都是。的子类 SMTPException。
#     auth_user：用于向SMTP服务器进行身份验证的可选用户名。如果没有提供，Django将使用该EMAIL_HOST_USER设置的值 。
#     auth_password：用于验证SMTP服务器的可选密码。如果没有提供，Django将使用该EMAIL_HOST_PASSWORD设置的值 。
#     connection：用于发送邮件的可选电子邮件后端。如果未指定，将使用默认后端的实例。有关 更多详细信息，请参阅电子邮件后端的文档。
#     html_message：如果html_message被提供，所得到的电子邮件将是一个 多部分/替代电子邮件message作为 文本/无格式内容类型和html_message作为 text / html的内容类型。
#
# 返回值将是成功传递消息的数量（可以是0或1因为它只能发送一条消息）。