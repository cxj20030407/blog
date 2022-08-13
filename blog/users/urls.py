from django.urls import path
from users.views import RegisterView, ImageCodeView
from users import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('imagecode/', ImageCodeView.as_view(), name='imagecode'),

    #用户注册
    path('user/register/', views.user_register),
    #用户登录
    path('user/login/', views.user_login),
    #验证码
    path('image/code/', views.image_code),
    #markdown编辑器
    path('editor/', views.editor),

]