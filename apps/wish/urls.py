from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.index),
    url(r'^registerprocess$', views.register),
    url(r'^loginprocess$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^wish_items/create$', views.create),
    url(r'^create$', views.create),
    url(r'^addWishProcess$', views.addWish),
    url(r'^logout$', views.logout),
    url(r'^wish_item/(?P<id>\d+)$', views.wish_item),
    url(r'^removeFromList/(?P<id>\d+)$', views.remove),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^item/(?P<id>\d+)$', views.item)



    # url(r'^addWishProcess$', views.ad),
]
