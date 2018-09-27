from django.conf.urls import url

from goods.views import Index, CategroyView, DetailsVeiw

urlpatterns=[
    url(r'^index/$',Index.as_view(),name='index'),
    url(r'^categroy/(?P<cate_id>\d+)/(?P<order>\d)/$',CategroyView.as_view(),name='CategroyView'),
    url(r'^detail/(?P<id>\d+)/$',DetailsVeiw.as_view(),name='DetailsVeiw'),
]