from django.shortcuts import render


# Create your views here.
from django.views import View

from db.base_view import BaseVerifyVeiw
from goods.models import GoodsSKU


class Index(View):
    def get(self,request):
        return render(request,'goods/index.html')

    def post(self,request):
        return render(request, 'goods/index.html')


class CategroyView(BaseVerifyVeiw):
    def get(self,request):
        #商品SKU模块:
        #找出要显示的所有sku商品:
        goods_sku=GoodsSKU.objects.filter(is_delete=False)
        #渲染到页面:
        return render(request,'goods/category.html',{'goods_sku':goods_sku})

    def post(self,request):
        return render(request,'goods/category.html')




class DetailsVeiw(BaseVerifyVeiw):
    def get(self,request,id):
        # 接收
        id = int(id)
        # 处理
        goods_sku = GoodsSKU.objects.filter(pk=id).first()
        # 响应
        return render(request, 'goods/detail.html', {'goods_sku': goods_sku})



    def post(self,request):
        return render(request, 'goods/detail.html')
