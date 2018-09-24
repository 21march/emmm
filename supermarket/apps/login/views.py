from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.

# 主页
from django.urls import reverse
from django.views import View

from db.base_view import BaseVerifyVeiw
from login.forms import LoginModelForm, RegisterModelForm, InfoModelForm
# from login.models import Login
from login.models import User


# 注册:
class RegisterView(View):
    # 注册功能
    def get(self, request):
        form = RegisterModelForm()
        return render(request, 'spuser/reg.html', {'form': form})

    def post(self, request):
        # 生成一个随机的验证码:
        session_code = request.session.get('random_code')
        # 强制转换为字典
        data = request.POST.dict()
        data['sesson_code'] = session_code
        # 从form表单得到数据,然后存入数据库
        # data = request.POST
        # 实例化一个form对象:
        form = RegisterModelForm(data)
        if form.is_valid():
            # 数据合法,保存:
            form.save()
            return render(request, 'spuser/member.html')
        else:
            # 数据不合法,提示错误信息,并留在当前页面
            return render(request, 'spuser/reg.html', {'form': form})


# 验证码:
class SendCodeView(View):
    """
    发送验证码
    """

    def post(self, request):
        # 1.接收请求参数:
        phone = request.POST.get('phone', '')
        # 2.处理数据:
        # 手机号码格式判断,正则判断
        import re
        # 设置正则的规则
        phone_re = re.compile('^1[3-9]\d{9}$')
        # 匹配 手机号码字符串
        res = re.search(phone_re, phone)
        if res is None:
            # 手机号码格式错误:
            return JsonResponse({'status': '400', 'msg': '手机号码格式错误.'})
        # 先格式,后看是否已经注册;
        res = User.objects.filter(phone=phone).exists()
        if res:
            # 手机号码已经注册:
            return JsonResponse({'status': '400', 'msg': '手机号码已经注册'})

        # 手机号码格式正确,并且未注册,生成随机验证码
        import random
        random_code = "".join([str(random.randint(0, 9)) for _ in range(4)])
        print('验证码为:{}'.format(random_code))

        # 将生成的随机验证码保存到session中:
        request.session['random_code'] = random_code
        request.session.set_expiry(60)

        # 3.响应
        return JsonResponse({'status': '200'})

    def get(self, request):
        pass


# 登录
class LoginView(View):
    # 登录功能
    def get(self, request):
        form = LoginModelForm()
        return render(request, 'spuser/login.html', {'form': form})

    def post(self, request):
        # 实例化一个表单对象:
        data = request.POST
        form = LoginModelForm(data)
        # a = form.is_valid()
        if form.is_valid():
            user = form.cleaned_data.get('user')
            request.session['ID'] = user.pk
            request.session['phone'] = user.phone
            request.session.set_expiry(0)

            return redirect(reverse('user:center'))
        return render(request, 'spuser/login.html', {'form': form})
        # 数据合法,与数据库中做对比:
        # cleaned_data=form.cleaned_data
        # phone=cleaned_data.get('phone')
        # password=cleaned_data.get('password')
        # 比较传入与数据库中的数据是否相同:
        # filter出来是一个查询集,加上first之后才会变成一个对象,才可以去出其中的字段
        # is_login=User.objects.filter(phone=phone,password=password).first()

        # if is_login:
        # 保存登录标识到session:
        # request.session['ID']=is_login.pk
        # request.session['phone']=is_login.phone
        # 设置有效期,关闭浏览器就失效:
        # request.session.set_expiry(0)
        # 跳转至用户中心:
        #         return redirect(reverse('user:center'))
        #     else:
        #         #比较失败,依然在login:
        #         return render(request,'spuser/login.html',{'form':form})
        # else:
        #     return render(request,'spuser/login.html',{'form':form})


class CenterView(BaseVerifyVeiw):
    # 个人中心功能
    def get(self, request):
        id = request.session.get('ID')
        user = User.objects.filter(pk=id).first()
        return render(request, 'spuser/member.html', {'user': user})

    def post(self, request):
        pass


class InforView(BaseVerifyVeiw):
    # 个人资料功能
    def get(self, request):
        # 得到当前登录账号的在session中的ID:
        user_id = request.session.get('ID')
        # 在数据库中查找到响应的用户
        user = User.objects.filter(pk=user_id).first()
        # 回显数据,通过:
        return render(request, "spuser/infor.html", {'user': user})

    def post(self, request):
        # 接收数据,保存到数据库:
        id = request.session.get('ID')
        data = request.POST
        file = request.FILES['head']
        # 处理数据，更新用户头像:
        user = User.objects.get(pk=id)
        user.head = file
        user.save()
        # form=InfoModelForm(data)
        # if form.is_valid():
        #     form.save()
        #     return render(request,'spuser/member.html')
        # else:
        #     context={
        #         'form':form
        #     }
        # return redirect(reverse('user:center'))
        return HttpResponse('ok')


class LogoutView(View):
    # 退出功能
    def get(self, request):
        pass

    def post(self, request):
        pass


def index(request):
    return render(request, 'spuser/index.html')


class AddressView(BaseVerifyVeiw):
    def get(self, request):
        return render(request, 'spuser/address.html')

    def post(self, request):
        # 保存收货地址:
        pass
