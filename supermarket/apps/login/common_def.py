import hashlib

from django.shortcuts import redirect
from django.urls import reverse

from supermarket import settings


def set_password(pwd):
    #为避免密码过于简单,加入一串字符再行加密:
    token=settings.SECRET_KEY
    password=token + pwd
    h=hashlib.md5(password.encode('utf-8'))
    return h.hexdigest()

#登录
def verify_login_required(func):
    #func:旧函数
    #定义一个新函数:

    def verify_login(request,*args,**kwargs):
        if request.session.get('ID') is None:
            #没有登录:
            return redirect(reverse('user:login'))
        else:
            return func(request,*args,**kwargs)

    return verify_login