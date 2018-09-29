from django.conf.urls import url


from shopping.views import AddCartView, DelCarView, CarShowView, TureOrderView

urlpatterns=[
    # url(r'^CategoryView/$',CategoryView.as_view(),name='CategoryView'),
    # url(r'^OrderView/$',OrderView.as_view(),name='OrderView'),
    url(r'^TureOrderView/$',TureOrderView.as_view(),name='TureOrderView'),
    # url(r'^PayView/$',PayView.as_view(),name='PayView'),
    # url(r'^ShopCartView/$',ShopCartView.as_view(),name='ShoCartView'),
    url(r'^AddCartView/$',AddCartView.as_view(),name='AddCartView'),
    url(r'^DelCarView/$',DelCarView.as_view(),name='DelCarView'),
    url(r'^CarShowView/$',CarShowView.as_view(),name='CarShowView'),
]