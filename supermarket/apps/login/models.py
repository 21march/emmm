from django.core import validators
from django.db import models


# Create your models here.
# 用户模型:
class User(models.Model):
    sex_choice = (
        (1, '男'),
        (2, '女'),
        (3, '保密'),
    )
    phone = models.CharField(max_length=11,
                             verbose_name='手机号码',
                             # validators=[
                             #     validators.RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误!")
                             # ],
                             )
    name = models.CharField(max_length=20,
                            default='',
                            verbose_name='昵称',
                            )
    password = models.CharField(max_length=64,
                                verbose_name='密码',
                                )
    sex = models.SmallIntegerField(choices=sex_choice,
                                   default=3,
                                   verbose_name='性别',
                                   )
    school = models.CharField(default='',
                              max_length=50,
                              verbose_name='学校',
                              )
    hometown = models.CharField(max_length=100,
                                default='',
                                verbose_name='家乡',
                                )
    address = models.CharField(max_length=255,
                               default='',
                               verbose_name='详细地址',
                               )
    # head = models.ImageField(verbose_name='用户头像',
    #                          upload_to='head/%Y/%m',
    #                          default='default/infortx.png',
    #                          )
    birthday = models.DateField(verbose_name='出生日期',
                                null=True,
                                blank=True,
                                )
    is_delete = models.BooleanField(default=False,
                                    verbose_name='是否删除',
                                    )
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name="创建时间",
                                       )
    update_time = models.DateTimeField(verbose_name="更新时间",
                                       auto_now=True,
                                       )


    class Meta:
        db_table = 'user'


    def __str__(self):
        return self.phone


# class Reg_table(models.Model):
#     phone=models.CharField(max_length=13,
#                            verbose_name='手机号码')
#     password=models.CharField(max_length=13,
#                               verbose_name='密码')


# class Login(models.Model):
#     phone = models.CharField(max_length=13,
#                              verbose_name='手机号码')
#     password = models.CharField(max_length=13,
#                                 verbose_name='密码')
#
#     class Meta:
#         db_table = 'login'
#
#     def __str__(self):
#         return self.phone
