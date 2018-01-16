from django.conf.urls import url

from axf import views

urlpatterns = [

    url(r'^home/', views.home, name="home"),
    url(r'^mine/', views.mine, name="mine"),
    url(r'^market/$', views.urlToMarket, name="urlToMarket"),
    url(r'^market/(\d+)/(\d+)/(\d+)', views.market, name="market"),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^login/', views.login, name='login'),
    url(r'^dologin/', views.doLogin, name="doLogin"),
    url(r'^register/', views.register, name='register'),
    url(r'^doregister/', views.doregister, name='doregister'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^checkuser/', views.checkuser, name='checkuser'),
    url(r'^userInfoMod/', views.userInfoMod, name='userInfoMod'),
    url(r'^addtocart/', views.addtocart, name="addtocart"),
    url(r'^changeselect/', views.changeselect, name="changeselect"),
    url(r'^cartgoodssub/', views.cartgoodssub, name="cartgoodssub"),
    url(r'^genorder/', views.genorder, name="genorder"),
    url(r'^pay/(\d+)', views.pay, name="pay"),

]
