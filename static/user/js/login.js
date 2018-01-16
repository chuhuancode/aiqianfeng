function check() {
    var login_password = $('#login_password').val;
    var newpwd = md5(login_password);
    $('#login_password').val(newpwd);
    return true;
}