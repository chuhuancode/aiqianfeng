import hashlib

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import time
import random
from django.conf import settings
import os
# Create your views here.
from django.urls import reverse

from axf.models import Wheel, Mustbuy, Shop, Mainshow, FoodTypes, Goods, Nav, User, Cart, Order


# 主页

def home(request):
    title = '主页'
    # 查询主页面的数据
    wheels = Wheel.objects.all()
    # 查询导航数据
    navs = Nav.objects.all()
    # 查询第二个轮播数据
    mustbuys = Mustbuy.objects.all()
    # shop商店
    shops = Shop.objects.all()
    shops_more = shops[3:7]
    shops_rec = shops[7:11]
    # 查询mainshow
    mainshows = Mainshow.objects.all()

    context = {
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shops': shops,
        'shops_more': shops_more,
        'shops_rec': shops_rec,
        'mainshows': mainshows,
    }
    return render(request, 'axf/home/home.html', context=context)


# 闪送

def market(request, typeid, childcid, sort_rule):
    title = "闪送超市"
    # 查询所有类型
    foodtypes = FoodTypes.objects.all()

    if childcid == "0":
        goods_list = Goods.objects.filter(categoryid=typeid)
    else:
        # 查询所有商品
        goods_list = Goods.objects.filter(categoryid=typeid).filter(childcid=childcid)
    # 销量升序
    if sort_rule == "1":
        goods_list = goods_list.order_by("productnum")
    # 销量降序
    elif sort_rule == "2":
        goods_list = goods_list.order_by("-productnum")
    # 价格降序
    elif sort_rule == "3":
        goods_list = goods_list.order_by("-price")
    # 价格升序
    elif sort_rule == "4":
        goods_list = goods_list.order_by("price")
    # 综合排序
    else:
        pass

    # 根据typeid将 childtypenames获取出来
    foodtype = FoodTypes.objects.filter(typeid=typeid)

    # 创建一个默认值
    childetypenames = "全部分类:0"
    if len(foodtype) > 0:
        childetypenames = foodtype.first().childtypenames
    # 切割数据
    childtypenamelist = childetypenames.split("#")
    childtypenamelisttran = []
    # print(childtypenamelist)
    # 二次处理数据
    # [[“名称”,"id"],["名称":"id"], ]
    for item in childtypenamelist:
        itemtran = item.split(":")
        childtypenamelisttran.append(itemtran)

    # print(childtypenamelisttran)

    sort_rule_list = [["综合排序", "0"], ["销量升序", "1"], ["销量降序", "2"], ["价格最低", "3"], ["价格最高", "4"]]

    context = {
        "title": title,
        "foodtypes": foodtypes,
        "goods_list": goods_list[0:20],
        "childtypenameslist": childtypenamelisttran,
        "typeid": typeid,
        "childcid": childcid,
        "sort_rule_list": sort_rule_list,
    }
    return render(request, 'axf/market/market.html', context=context)


# 我的

def mine(request):
    # 配置基本信息
    title = '朕'
    usericon = ''
    # 获取session信息,
    username = request.session.get('username')
    # 判断是否登录
    if username == None:
        username = '未登录'
        # 未登录，给一个值，用于记录
        is_login = False
    else:
        is_login = True
        # 把用户名替换到登录那块
        user = User.objects.get(u_name=username)
        # 匹配路径,上传图片
        usericon = "http://127.0.0.1:8000/static/uploadfiles/" + user.u_icon.url

    context = {
        'title': title,
        'is_login': is_login,
        'username': username,
        'usericon': usericon,
    }
    return render(request, 'axf/mine/mine.html', context=context)


# 用户登录页面
def login(request):
    return render(request, 'axf/user/login.html')


# 登录验证
def doLogin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    """
            两种写法
                1，直接去数据库查询用户名和密码

                2，用用户名去查找，没找到提示用户名不存在
                用户名找到了再去验证密码，
        """
    user = User.objects.filter(u_name=username)
    if len(user) > 0:

        # 因为注册的时候在输入的时候就加密了，所以在登陆的时候需要要给他加密，让两个密码都进行加密比较
        # 比对加密密码，将密码进行hash算法后进行比较，
        # 导入库
        md5 = hashlib.md5()
        # 对密码编码
        md5.update(password.encode('utf-8'))
        # 加算法
        newpassword = md5.hexdigest()

        # u_passwd是model里面的获取密码
        if newpassword == user.first().u_passwd:
            # 密码成功，把用户名提交到登陆后的页面
            request.session['username'] = username
            # 登陆成功，跳转回个人中心
            response = HttpResponseRedirect(reverse('axf:mine'))
            return response
        else:
            return redirect(reverse('axf:login'))
    else:
        return redirect(reverse('axf:login'))


# 退出登录，两种清除方式，清除登录的信息，
def logout(request):
    # 1，用session清除
    del request.session['username']
    response = HttpResponseRedirect(reverse('axf:mine'))

    # ,2，用cookie清除
    # response.delete_cookie('sessionid')
    # response =  HttpResponseRedirect(reverse('axf:mine'))
    return response


# 注册页面
def register(request):
    return render(request, 'axf/user/register.html')


# 执行注册
def doregister(request):
    try:
        # /存储用户信息
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        # 这里要用[]
        icon = request.FILES['icon']
        print(password)

        # 获取摘要
        md5 = hashlib.md5()
        # 将原数据传入进行摘要计算， 元数据需要需要进行二进制格式
        md5.update(password.encode('utf-8'))
        # 获取摘要后的信息   hex 16进制    digest获取摘要输出
        # digest（）获取到的是二进制的输出   hexdigest（） 获取的是16进制输出，16进制可以直接转换成可见字符串
        p = md5.hexdigest()
        print(p)
        password = p

        user = User()
        user.u_name = username
        user.u_passwd = password
        user.u_email = email
        user.u_phone = phone
        user.u_icon = icon
        user.save()
        # 将用户个人信息存储在session里
        request.session['username'] = username
        return redirect(reverse('axf:mine'))

    except Exception as e:
        print('注册失败')
        return HttpResponse('注册失败')


# 检验用户名是否重复
def checkuser(request):
    uname = request.GET.get('uname')
    users = User.objects.filter(u_name=uname)

    if len(users) > 0:
        msg = '用户已存在'
        state = 300
    else:
        msg = '用户名可用'
        state = 200

    data = {'msg': msg, 'state': state}
    return JsonResponse(data)


# 个人信息
def userInfoMod(request):
    return render(request, 'axf/user/userInfoMod.html')


# 重定向闪送
def urlToMarket(request):
    return redirect(reverse("axf:market", args=["104749", "0", "0"]))


def cart(request):
    # 判断是否登录
    username = request.session.get('username')
    # 未登录
    if username == None:
        return redirect(reverse('axf:login'))
    # 已登录
    user = User.objects.get(u_name=username)
    carts = Cart.objects.filter(c_user=user).filter(c_belong=False)

    context = {
        'carts': carts,
    }
    return render(request, 'axf/cart/cart.html', context)


def addtocart(request):
    # 判断用户是否登录
    username = request.session.get('username')
    # 用户未登录
    if username == None:
        # 跳转到登录页面
        return redirect(reverse('axf:login'))
    # 用户已登录，数据添加到登录车
    goods_id = request.GET.get('goodsid')
    # 通过ID将商品添加到商品的的表里
    goods = Goods.objects.get(pk=goods_id)
    # 获取用户登录信息
    user = User.objects.get(u_name=username)

    # 购物车数量增加
    c = Cart.objects.filter(c_user=user).filter(c_goods=goods).filter(c_belong=False)
    if len(c) == 0:
        c = Cart()
    else:
        c = c.first()
        num = c.c_goods_num
        c.c_goods_num = num + 1
    # 存储购物信息
    c.c_user = user
    c.c_goods = goods
    c.save()
    return JsonResponse({'msg': '添加成功'})


def changeselect(request):
    cartid = request.GET.get('cartid')
    cartselected = request.GET.get('cartselected')
    # print(cartid)
    # print(cartselected)
    car = Cart.objects.get(pk=cartid)
    car.c_selected = not cartselected
    car.save()

    return JsonResponse({'msg': 'ok'})


# 购物车数量减1
def cartgoodssub(request):
    cartid = request.GET.get('cartid')
    car = Cart.objects.get(pk=cartid)
    num = car.c_goods_num
    if num == 1:
        #  删除此条数据
        car.delete()
    else:
        car.c_goods_num = num - 1
        car.save()

    return JsonResponse({'num': num - 1, 'msg': 'ok'})


# 生成订单
def genorder(request):
    cartids = request.GET.get('cartids')
    # 列表拆分
    cartids = cartids.split('#')
    # print(cartids)

    # 生成订单  将要购买的商品转换到订单表中，生成订单信息，将购买的商品的订单信息关联
    order = Order()
    username = request.session.get('username')
    user = User.objects.get(u_name=username)
    #
    order.o_user = user
    # 定义状态 0，默认生成状态 ， 1 ，已下单未付款 ， 2 已付款  ，3 已付款并已发货....
    order.o_status = 1
    order.save()
    # order 在存储之后就有id了
    for item in cartids:
        car = Cart.objects.get(pk=item)
        #  修改属于那张表
        car.c_belong = True
        car.c_order = order
        car.save()

    return JsonResponse({'msg': 'ok', 'orderid': order.id})


# 支付，相关平台注册开发者账号，配置自己的信息     ping++可以快速集成多种支付
def pay(request, orderid):
    context = {
        "orderid": orderid,
    }
    return render(request, 'axf/order/pay.html', context)
