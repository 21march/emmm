from django import forms

from login.common_def import set_password
from login.models import User


class LoginModelForm(forms.ModelForm):
    #登录的form
    class Meta:
        model = User
        fields = ['phone', 'password']

        widgets={
            'phone':forms.TextInput(attrs={"class":"login-name","placeholder":"请输入用户名/手机号"}),
            'password':forms.PasswordInput(attrs={"class":"login-password","placeholder":"请输入密码"})
        }

        error_messages={
            'phone':{
                'required':'电话号码必填',
            },
            'password':{
                'required':'密码必填',
            }
        }


    def clean(self):
        # pass
        cleaned_data=super().clean()
        #验证手机和密码是否正确:
        phone=cleaned_data.get('phone')
        password=cleaned_data.get('password')
        #通过手机号查询数据,如果有再验证密码,没有则直接报错:
        user=User.objects.filter(phone=phone).first()
        if user is None:
            #手机号未注册:
            raise forms.ValidationError({'phone':'该手机号码未注册.'})
        else:
            #验证密码是否正确:
            password_in_db=user.password #已经加密的password
            password=set_password(password)
            if password_in_db != password:
                #密码错误:
                raise forms.ValidationError({'password':'密码错误.'})
            else:
                #保存用户的信息对象到 cleaned_data,以便之后视图调用:
                cleaned_data['user']=user
                return cleaned_data




class RegisterModelForm(forms.ModelForm):

    #确认密码
    repassword=forms.CharField(max_length=16,
                               min_length=6,
                               error_messages={
                                   'required':'请填写确认密码',

                               },
                               widget=forms.PasswordInput(attrs={'class':'login-password',
                                                                 'placeholder':'请输入确认密码'}),
                               )
    class Meta:
        model=User
        fields=['phone','password']

        widgets={
            'phone':forms.TextInput(attrs={'class':'login-name','placeholder':'请输入手机号'}),
            'password':forms.PasswordInput(attrs={'class':'login-password','placeholder':'请输入密码'})
        }
        error_messages = {
            'phone': {
                'required': '电话号码必填',
                # 'max_length': '字数不能超过13',
            },
            'password': {
                'required': '密码必填',
                'max_length': '不能超过16个字符',
                'min_length':'不能少于6个字符',
            }
        }


    #不可重复注册,验证手机号码是否已被注册,对手机号码的单个验证:
    def clean_phone(self):
        phone=self.cleaned_data.get('phone')  #传入的手机号码
        #查询数据库:
        is_reg=User.objects.filter(phone=phone).exists()
        if is_reg:
            #已经被注册:
            raise forms.ValidationError('该手机号码已经被注册')
        #返回清洗后的字段
        return phone




    #综合验证,验证密码和确认密码是否相等:
    def clean(self):
        #所有清洗后的数据:
        cleaned_data=super().clean()

        pwd1=cleaned_data.get('password')
        pwd2=cleaned_data.get('repassword')
        #比较是否相等:
        if pwd1 and pwd2 and pwd1 != pwd2:
            #两者都有,且不相等,抛出异常:
            raise forms.ValidationError({'repassword':'两次密码不一致'})
        else:
            if pwd1:
                #有密码才会加密:
                cleaned_data['password']=set_password(pwd1)
        return cleaned_data

class InfoModelForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['phone','name','sex','school','hometown']



class AddressModelForm(forms.ModelForm):
    class Meta:
        pass
        # model=