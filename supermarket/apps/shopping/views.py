# from django.shortcuts import render
#
# # Create your views here.
# from django.views import View
#
from django.shortcuts import render

from db.base_view import BaseVerifyVeiw



class TureOrderView(BaseVerifyVeiw):
    def get(self,request):
        return render(request, 'shopping/tureorder.html')

    def post(self,request):
        return render(request,'shopping/tureorder.html')
#
#
#
# class OrderView(BaseVerifyVeiw):
#     def get(self,request):
#         return render(request, 'shopping/order.html')
#
#     def post(self,request):
#         return render(request,'shopping/order.html')
#
#
#
# class PayView(BaseVerifyVeiw):
#     def get(self, request):
#         return render(request, 'shopping/pay.html')
#
#     def post(self, request):
#         return render(request, 'shopping/pay.html')
#
#
# class CategoryView(BaseVerifyVeiw):
#     def get(self,request):
#         return render(request,'shopping/category.html')
#     def post(self,request):
#         return render(request, 'shopping/category.html')
#
#
# class ShopCartView(BaseVerifyVeiw):
#     def get(self, request):
#         return render(request, 'shopping/shopcart.html')
#
#     def post(self, request):
#         return render(request, 'shopping/shopcart.html')
from django.http import JsonResponse
from django.views import View

from goods.models import GoodsSKU
from django_redis import get_redis_connection

from shopping.helper import get_car_key

"""
    添加购物车
    1. 使用post方式
    2. post中完成的内容
        a. 首先判断是否登录
            user_id = request.session.get("ID")

            没有登录,跳转到登录页面

        a. 接收参数 request.POST
            参数:
                sku_id 商品sku_id
                count 添加的数量

            判断参数的合法性:
                1. 都要是整数
                2. 商品必须要存在
                3. 库存判断

        b. 每个人的购物车都不一样
            如何确保每个人购物车不一致(购物车放redis)
            链接redis, 操作

            使用redis中的hash对象保存购物车
            hset key field value
            hset car_user_id sku_id count sku_id2 count2  ...........
            每条记录都要有两个字段
            sku_id 
            count 


            添加购物车的时候, 有两种情况:
                判断购物车中是否有sku_id,如果有在元有的基础上 对count进行添加,
                没有直接添加
        c. 添加成功 返回
            该用户购物车中商品的总数量

"""


class AddCartView(View):
    def get(self, request):
        pass

    def post(self, request):
        # 判断是否登录:
        user_id = request.session.get('ID')
        if user_id is None:
            #             没登录
            return JsonResponse({'error': 1, 'msg': '未登录,请先登录.'})

        # 登录了,接收参数:
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        # 判断参数是否合法:
        # 1.整数:
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            return JsonResponse({'error': 2, 'msg': '参数错误'})
        # 商品是否存在:
        try:
            goods_sku = GoodsSKU.objects.get(pk=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'error': 3, 'msg': '商品不存在'})

        # 库存:
        if goods_sku.stock < count:
            # 库存不足:
            return JsonResponse({'error': 4, 'msg': '库存不足'})

        # 将购物车数据存入redis中:
        # 连接redis.导入,
        cnn = get_redis_connection('default')
        # 操作redis:
        # 准备:
        car_key = get_car_key(user_id)
        # cnn.hset(car_key,sku_id,count)
        cnn.hincrby(car_key, sku_id, count)

        # 获取购物车中的总商品数
        car_values = cnn.hvals(car_key)  # 保存到Redis中的数据是二进制,需要解码才可以使用
        total = 0
        for v in car_values:
            total += int(v)

        return JsonResponse({'error': 0, 'msg': '添加成功', 'total': total})


"""
减购物车
"""


class DelCarView(View):
    def get(self, request):
        pass

    def post(self, request):
        # 1.判断是否登录
        user_id = request.session.get('ID')
        if user_id is None:
            #             没登录
            return JsonResponse({'error': 1, 'msg': '未登录,请先登录.'})

            # 登录了,接收参数:
        sku_id = request.POST.get('sku_id')
        count = -1

        # 判断参数是否合法:
        # 1.整数:
        try:
            sku_id = int(sku_id)
        except:
            return JsonResponse({'error': 2, 'msg': '参数错误'})
        # 商品是否存在:
        try:
            goods_sku = GoodsSKU.objects.get(pk=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'error': 3, 'msg': '商品不存在'})

        # 从购物车中减去商品
        # 连接Redis:
        cnn = get_redis_connection('default')

        # 操作Redis,准备key
        car_key = get_car_key(user_id)
        # 从购物车的数量减
        cnn.hincrby(car_key, sku_id, count)

        # 如果sku_id对应数量为0,就从购物车中删除sku_id
        count = cnn.hget(car_key, sku_id)
        if int(count) < 1:
            cnn.hdel(car_key, sku_id)

        # 获取购物车中的商品总数:

        car_values = cnn.hvals(car_key)

        total = 0
        for v in car_values:
            total += int(v)

        return JsonResponse({'error': 0, 'msg': '减少成功', 'total': total})


"""
购物车展示页面
"""


class CarShowView(BaseVerifyVeiw):
    def get(self, request):
        """
        获取购物车数据:
        1.购物车中的商品数据:
        存放在Redis中 sku_id count
        根据sku_id 查询出商品数据

        返回一个列表,有所有的商品数据


        2.所有商品的总价格和总数量
        :param request:
        :return:
        """
        user_id = request.session.get('ID')

        # 准备两个变量
        total_price = 0  # 总价
        total_count = 0  # 总数
        # 得到购物车中的商品数据,从Redis中获取
        cnn = get_redis_connection('default')
        # 准备car_key:
        car_key = get_car_key(user_id)
        # 取数据:
        cars = cnn.hgetall(car_key)
        # print(cars)  {b'4': b'5', b'2': b'2'}  字典

        # 遍历:
        goodslist = []
        for sku_id, count in cars.items():
            # print(sku_id,count)
            sku_id = int(sku_id)
            count = int(count)

            # 通过sku_id 获取商品信息
            goods_sku = GoodsSKU.objects.get(pk=sku_id)

            # 对应商品本来无count属性,现在需要加入一个count属性
            goods_sku.count = count

            goodslist.append(goods_sku)

            # 总价:
            total_price += goods_sku.price * count
            total_count += count

        context = {
            'total_price': total_price,
            'total_count': total_count,
            'goodslist': goodslist,

        }

        return render(request, 'shopping/shopcart.html', context)

    def post(self, request):
        pass

