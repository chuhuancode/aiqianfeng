/**
 * Created by chu on 17-12-20.
 */
$(function () {
    //用户名   blur失去焦点，获取输入框的内容，需要将框中的内容发送给服务器去验证
    $('#register_username').blur(function () {
        var uname = $(this).val()
        //用ajks获取,向服务器发送用户名进行验证
        //第一个参数，访问的域名，第二个参数，需要得到的数据，然后回调函数，请求服务器返回的数据
        $.getJSON('http://127.0.0.1:8000/axf/checkuser/', {'uname': uname}, function (data) {
            console.log(data['state']);
            console.log(data['msg']);

            if (data['state'] == 200) {
                $('#username_check').css('color', '#00ff00');
            } else if (data['state'] == 300) {
                $('#username_check').css('color', '#ff0000');
            }
            $('#username_check').html(data['msg'])
        })
    })
})


function check() {

//    在这里做提交钱的验证，验证密码和确认密码
//    获取密码和第二次传入的密码
    var pwd = $('#register_password').val();
    //  获取第二次传入的密码
    var pwdc = $('#register_password_confirm').val();
    if (pwd == pwds) {
        $('#password_check').html('两次密码一致');
        $('#password_check').css('color', '#00ff00');
    } else {
        $('#password_check').html('两次密码不一致');
        $('#password_check').css('color', '#ff0000');
        return false;
        //    false,校验，必填，true，可以为空，很多网站的注册信息都是这么做的
        //    必填选项和可以为空选项
    }

    //登录密码加密
    var newPwd = md5(pwd);
    $("#register_password").val(newPwd);
    return true;
}



