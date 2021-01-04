from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.contrib.auth import authenticate,login
# Django 提供内置的视图(view)函数用于处理登录和退出,
# Django提供两个函数来执行django.contrib.auth中的动作 : authenticate()和login()。

# 认证给出的用户名和密码，使用 authenticate() 函数。它接受两个参数，用户名 username 和 密码 password ，
# 并在密码对给出的用户名合法的情况下返回一个 User 对象。 如果密码不合法，authenticate()返回None。
from django.contrib.auth.backends import ModelBackend
from users.models import UserProfile,EmailVerifyecord
from django.db.models import Q

from django.views.generic.base import View
from users.form import LoginForm,RegisterForm,ForgetPwdForm,ModifyPwdForm
from apps.utils.email_send import send_register_eamil

# Create your views here.


# 邮箱和用户名都可以登录
# 基础ModelBackend类，因为它有authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个，两个时get失败的一种原因Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))

            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    '''用户登录'''

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 实例化
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 获取用户提交的用户名和密码
            user_name = request.POST.get('username', None)
            pass_word = request.POST.get('password', None)
            # 成功返回user对象,失败None
            user = authenticate(username=user_name, password=pass_word)
            # 如果不是null说明验证成功
            if user is not None:
                if user.is_active:
                    # 只有注册激活才能登录
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})
            # 只有当用户名或密码不存在时，才返回错误信息到前端
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})

        # form.is_valid（）已经判断不合法了，所以这里不需要再返回错误信息到前端了
        else:
            return render(request, 'login.html', {'login_form': login_form})

# 激活用户
# 根据邮箱找到对应的用户，然后设置is_active = True来实现
class ActiveUserView(View):
    def get(self,request,active_code):
        # 查询邮箱是否已经存在
        all_record = EmailVerifyecord.objects.filter(code= active_code)

        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功跳转到登录页面
                return render(request, 'login.html')


class RegisterView(View):
    '''用户注册'''
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', None)
            # 如果用户已存在，则提示错误信息
            if UserProfile.objects.filter(email = user_name):
                return render(request, 'register.html', {'register_form':register_form,'msg': '用户已存在'})

            pass_word = request.POST.get('password', None)
            # 实例化一个user_profile对象
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # 对保存到数据库的密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_eamil(user_name,'register')
            return render(request,'login.html')
        else:
            return render(request,'register.html',{'register_form':register_form})

# 说明：
#
#     如果是get请求，直接返回注册页面给用户
#     如果是post请求，先生成一个表单实例，并获取用户提交的所有信息（request.POST）
#     is_valid()方法，验证用户的提交信息是不是合法
#     如果合法，获取用户提交的email和password
#     实例化一个user_profile对象，把用户添加到数据库
#     默认添加的用户是激活状态（is_active=1表示True），在这里我们修改默认的状态（改为is_active = False），只有用户去邮箱激活之后才改为True
#     对密码加密，然后保存，发送邮箱，username是用户注册的邮箱，‘register’表明是注册
#     注册成功跳转到登录界面


class ForgetPwdView(View):
    '''找回密码'''
    def get(self,request):
        forget_from = ForgetPwdForm()
        return render(request,'forgetpwd.html',{'forget_from':forget_from})

    def post(self,request):
        forget_from = ForgetPwdForm(request.POST)
        if forget_from.is_valid():
            email = request.POST.get('email', None)
            send_register_eamil(email, 'forget')

        else:
            return render(request, 'forgetpwd.html',{'forget_form': forget_from})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email":email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email":email, "msg":"密码不一致！"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email":email, "modify_form":modify_form })