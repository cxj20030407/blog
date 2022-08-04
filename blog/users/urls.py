from django.urls import path
from users.views import RegisterView, ImageCodeView
from users.views import user_register, user_login, image_code

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('imagecode/', ImageCodeView.as_view(), name='imagecode'),

    #用户注册
    path('user/register/', user_register),
    #用户登录
    path('user/login/', user_login),
    #验证码
    path('image/code/', image_code),

]