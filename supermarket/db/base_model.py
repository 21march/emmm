from django.db import models

class BaseModel(models.Model):
    create_time=models.DateTimeField(auto_now_add=True,
                                     verbose_name='添加时间',
                                     )
    update_time=models.DateTimeField(verbose_name='更新时间',
                                     auto_now=True,
                                     )
    is_delete=models.BooleanField(verbose_name='是否删除',
                                  default=False,
                                  )
    class Meta:
        abstract=True