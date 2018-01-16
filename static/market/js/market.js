$(function () {
//类型过滤
    $("#all_type").click(function () {
        // alert("全部类型");
        $("#all_type_content").css("display", "block")
        $("#all_type_content").click(function () {
            $(this).css("display", "none");
        })
    })


//结果集排序规则
    $("#sort_rule").click(function () {
        // alert("排序规则");
        $("#sort_rule_content").css("display", "block").click(function () {
            $(this).css("display", "none");
        })
    })
//------------------------------------------


    //商品加到购物车
    $('.goods_add').click(function () {
        // alert('hhhhh')
        //  将商品数据发送到服务器中，添加到购车里，将商品id发送到服务器
        // alert($(this).attr('goods_id'));
        var goods_id = $(this).attr('goods_id');
        //写地址的时候，浏览器上写ip就写ip，使用的域名就写域名
        //用ajks发送请求
        $.get('http://127.0.0.1:8000/axf/addtocart/', {'goodsid': goods_id}, function (data) {
            alert(data['msg']);

        })
    })

})