from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from db.base_model import BaseModel

is_on_sale = (
    (0, '下架'),
    (1, '上架')
)


class Categroy(BaseModel):
    cate_name = models.CharField(verbose_name='分类名称',
                                 max_length=20,
                                 )
    brief = models.CharField(verbose_name='描述',
                             max_length=200,
                             null=True,
                             blank=True,
                             )

    def __str__(self):
        return self.cate_name

    class Meta:
        verbose_name = '商品分类管理'
        verbose_name_plural = verbose_name


class Unit(BaseModel):
    """
    商品Sku单位  最小单位,
    """
    name = models.CharField(max_length=20,
                            verbose_name='单位')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商品单位管理'
        verbose_name_plural = verbose_name


class GoodsSPU(BaseModel):
    """
    SPU表,相当于一个大的分类
    """
    spu_name = models.CharField(verbose_name='商品SPU名称',
                                max_length=20,
                                )
    # content = models.TextField(verbose_name='商品详情')

    content=RichTextUploadingField(verbose_name="商品详情")


    def __str__(self):
        return self.spu_name

    class Meta:
        verbose_name = '商品SPU(大分类)管理'
        verbose_name_plural = verbose_name


class GoodsSKU(BaseModel):
    """
    sku表:某个spu下的具体型号的
    """
    sku_name = models.CharField(verbose_name='商品SKU名称',
                                max_length=100,
                                )
    brief = models.CharField(verbose_name='商品简介',
                             max_length=200,
                             null=True,
                             blank=True,
                             )
    price = models.DecimalField(verbose_name='价格',
                                max_digits=9,
                                decimal_places=2,
                                default=0,
                                )
    unit = models.ForeignKey(to='Unit',
                             verbose_name='单位',
                             )
    stock = models.IntegerField(verbose_name='库存',
                                default=0,
                                )
    sale_num = models.IntegerField(verbose_name='销量',
                                   default=0,
                                   )
    logo = models.ImageField(verbose_name='封面图片',
                             upload_to='goods/%Y%m/%d',
                             )
    is_on_sale = models.BooleanField(verbose_name='是否上架',
                                     choices=is_on_sale,
                                     default=0,
                                     )
    category = models.ForeignKey(to='Categroy',
                                 verbose_name='商品分类',  # 大的分类,如电子产品
                                 )
    goods_spu = models.ForeignKey(to='GoodsSPU',
                                  verbose_name='商品SPU名称',  # 电子产品下的分类,如荣耀10
                                  )

    def __str__(self):
        return self.sku_name

    class Meta:
        verbose_name = '商品SKU名称'
        verbose_name_plural = verbose_name


class Gallery(BaseModel):
    """
    商品相册
    """
    img_url = models.ImageField(upload_to='goods_gallery/%Y%m/%d',
                                verbose_name='商品相册路径',
                                )
    goods_sku = models.ForeignKey(to='GoodsSKU',
                                  verbose_name='SKU名称')

    class Meta:
        verbose_name = '商品相册管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '商品:%s的相册' % self.goods_sku.sku_name


class Banner(BaseModel):
    """
    首页轮播
    """
    name = models.CharField(verbose_name='商品活动名',
                            max_length=150,
                            )
    goods_sku = models.ForeignKey(to='GoodsSKU',
                                  verbose_name='SKU商品',
                                  )
    img_url = models.ImageField(verbose_name='轮播图片地址',
                                upload_to='banner/%Y%m/%d'
                                )
    order = models.SmallIntegerField(verbose_name='排序',
                                     default=0,
                                     )

    class Meta:
        verbose_name = '首页轮播管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Activity(BaseModel):
    """
    首页活动
    """
    title = models.CharField(verbose_name='活动名称',
                             max_length=150,
                             )
    img_url = models.ImageField(verbose_name='活动图片地址',
                                upload_to='activity/%Y%m/%d',
                                )
    url_site = models.CharField(verbose_name='活动的url地址',
                                max_length=200,
                                )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '商品活动管理'
        verbose_name_plural = verbose_name


class ActivityZone(BaseModel):
    """
    首页活动专区
    """
    title = models.CharField(verbose_name='活动标题',
                             max_length=100,
                             )
    brief = models.CharField(verbose_name='活动专区简介',
                             max_length=255,
                             null=True,
                             blank=True,
                             )
    order = models.SmallIntegerField(verbose_name='排序',
                                     default=0,
                                     )
    is_on_sale = models.SmallIntegerField(verbose_name='是否上架',
                                          choices=is_on_sale,
                                          default=0,
                                          )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '首页活动专区管理'
        verbose_name_plural = verbose_name


class ActivityZoneGoods(BaseModel):
    """
        首页活动专区商品列表
    """
    activity_zone = models.ForeignKey(to="ActivityZone",
                                      verbose_name="活动专区ID",
                                      )
    goods_sku = models.ForeignKey(to="GoodsSKU",
                                  verbose_name="专区商品SKU_ID",
                                  )
