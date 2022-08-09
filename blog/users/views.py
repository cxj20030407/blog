from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
# from utils.response_code import RETCODE
# from random import randint
# from libs.yuntongxun.sms import CCP
import logging
import re
from users.models import User
from django.db import DatabaseError
from django.contrib.auth import login, authenticate
logger=logging.getLogger('django')

# 注册视图
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    def post(self, request):
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        smscode = request.POST.get('sms_code')
        if not all([mobile, password, password2, smscode]):
            return HttpResponseBadRequest('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('请输入正确的手机号码')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseBadRequest('请输入8-20位的密码')
        if password != password2:
            return HttpResponseBadRequest('两次输入的密码不一致')
        redis_conn = get_redis_connection('default')
        redis_sms_code = redis_conn.get('sms:%s' % mobile)
        if redis_sms_code is None:
            return HttpResponseBadRequest('短信验证码已过期')
        if smscode != redis_sms_code.decode():
            return HttpResponseBadRequest('短信验证码错误')
        try:
            user = User.objects.create_user(username=mobile, mobile=mobile, password=password)
        except DatabaseError as e:
            logger.error(e)
            return HttpResponseBadRequest('注册失败')
        return HttpResponse('注册成功，重定向到首页')

# 验证码视图
class ImageCodeView(View):

    def get(self, request):
        uuid = request.GET.get('uuid')
        if uuid is None:
            return HttpResponseBadRequest('请求参数错误')
        text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection('default')
        redis_conn.setex('img:%s'%uuid, 300, text)
        return HttpResponse(image, content_type='image/jpeg')


# ########################### 测试版本 ###############################
from io import BytesIO
from users import models
from users.utils.form import LoginForm
from users.utils.code import check_code

# 登录视图
def user_login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证码的校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})

        # 去数据库校验用户名和密码是否正确
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        # print(form.cleaned_data)
        # print(admin_object)
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串，写到用户浏览器的cookie中，再写入到session中；
        request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        # return redirect("/admin/list/")
        return redirect("/register/")

    return render(request, 'login.html', {'form': form})

def image_code(request):
    """ 生成图片验证码 """

    img, code_string = check_code()

    # 写入到自己的session中
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())

def user_register(request):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})