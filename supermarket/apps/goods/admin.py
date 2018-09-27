from django.contrib import admin

from goods.models import Categroy, Unit, GoodsSPU, GoodsSKU, Gallery, Banner, ActivityZoneGoods, ActivityZone

# Register your models here.

admin.site.site_header = '超市管理平台'


@admin.register(Categroy)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass


@admin.register(GoodsSPU)
class GoodsSPUAdmin(admin.ModelAdmin):
    # 商品SPU
    pass


# 关联商品的相册
class GoodsSKUAdminInLine(admin.TabularInline):
    model = Gallery
    extra = 3
    fields = ['goods_sku', 'img_url']


# 注册GoodsSKU的模型到后台
@admin.register(GoodsSKU)
# 定制显示效果
class GoodsSKUAdmin(admin.ModelAdmin):
    # 商品SPU
    # 关联模型展示
    inlines = [
        GoodsSKUAdminInLine
    ]



@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    pass



class ActivityZoneGoodsInline(admin.TabularInline):
    model=ActivityZoneGoods
    extra = 3
    fields = ['activity_zone', 'goods_sku']


@admin.register(ActivityZone)
class ActivityZoneAdmin(admin.ModelAdmin):
    inlines = [
        ActivityZoneGoodsInline
    ]