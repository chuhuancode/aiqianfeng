$(function () {
//    获取选想按钮
    $('.ischose').click(function () {
        //将当前选项的id发送给服务器
        var cart_id = $(this).attr('cartid');
        var cart_selected = $(this).attr('cartslected');
        if (cart_selected == 'True') {
            $(this).attr('cartselected', 'False');
        } else {
            $(this).attr('cartselected', 'True');
        }

        var child = $(this).find("span");
        $.getJSON('http://127.0.0.1:8000/axf/changeselect', {
            'cartid': cart_id,
            'cartslected': cart_selected
        }, function (data) {
            if (data['msg'] == 'ok') {
                $(child).toggle();
            }
        })
    })


    //购物车数量减1

    $('.subShopping').click(function () {
        //获取到点击项目的id
        var sub = $(this);
        var cartid = $(this).attr('cartid');
//将信息传递给服务器
        $.getJSON('http://127.0.0.1:8000/axf/cartgoodssub/', {'cartid': cartid}, function (data) {
            // alert(data['num'])
            if (data['num'] == 0) {
                //    删除,根据它自己找到父类，整个商品的信息，然后干掉
                sub.parents('li').remove();
            } else {
                //将num放到先输数据的地方
                sub.next('span').html(data['num']);

            }
        })
    })

//    添加下单点击

    $('#select_ok').click(function () {
        //    获取所有包含数据的item，内部选中为显示的获取出来
        var spans = $('.ischose').find('span');
        var cartids = [];

        for (var i = 0; i < spans.length; i++) {
            if ($(spans[i]).css('display') == 'block') {
                console.log($(spans[i]).attr('id'));
                //把选中的都推进去
                cartids.push($(spans[i]).attr('id'));
            }
        }
        // 向服务器传输数据
        console.log(cartids)
        $.getJSON("http://127.0.0.1:8000/axf/genorder/", {"cartids": cartids.join("#")}, function (data) {

            alert(data["msg"]);
            //    接收到订单id，拿着id进行页面跳转，去付款
            window.open("http://127.0.0.1:8000/axf/pay/" + data["orderid"], "_self");


        })
    })
})