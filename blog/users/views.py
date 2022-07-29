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