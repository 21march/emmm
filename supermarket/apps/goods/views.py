from django.shortcuts import render

# Create your views here.
from django.views import View

from db.base_view import BaseVerifyVeiw
from goods.models import GoodsSKU, Banner, Categroy, ActivityZoneGoods, ActivityZone


class Index(View):
    def get(self, request):
        # goods=ActivityZoneGoods.objects.filter(is_delete=False)
        activity=ActivityZone.objects.filter(is_delete=False)
        banners = Banner.objects.filter(is_delete=False)
        context = {
            'banners': banners,
            'activity':activity,
            # 'goods':goods,
        }
        return render(request, 'goods/index.html', context)

    def post(self, request):
        return render(request, 'goods/index.html')


"""
1.查询所有商品
2.查询出所有分类,并显示
3.点击某个分类显示对应的商品
url 传递分类的id ,先默认为0,展示第一个
4.排序

"""


class CategroyView(BaseVerifyVeiw):
    def get(self, request, cate_id=0,order=0):
        # 字符串转int:
        order=int(order)
        cate_id = int(cate_id)
        # 商品SKU模块:
        # 找出要显示的所有sku商品,和所有分类:
        # goods_sku=GoodsSKU.objects.filter(is_delete=False)
        categorys = Categroy.objects.filter(is_delete=False)
        # 找出对应分类下的商品,需要判断数字:
        if cate_id == 0:
            # goods_sku=GoodsSKU.objects.filter(pk=cate_id).first()
            category = categorys.first()

            cate_id=category.pk

        else:
            category = Categroy.objects.get(pk=cate_id)

        #设置映射关系:
        order_by_rule=["id", "-sale_num", "-price", "price", "-create_time"]
        goods_skus = category.goodssku_set.all().order_by(order_by_rule[order])

        # 渲染到页面:
        context = {
            'cate_id':cate_id,
            'goods_skus': goods_skus,
            'categorys': categorys,
            'order':order,
        }
        return render(request, 'goods/category.html', context)

    def post(self, request):
        return render(request, 'goods/category.html')


class DetailsVeiw(BaseVerifyVeiw):
    def get(self, request, id):
        # 接收
        id = int(id)
        # 处理
        goods_sku = GoodsSKU.objects.filter(pk=id).first()
        # 响应
        return render(request, 'goods/detail.html', {'goods_sku': goods_sku})

    def post(self, request):
        return render(request, 'goods/detail.html')
