function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $(".form-login").submit(function(e){
        //取消默认提交
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
            var data={};
            $(this).serializeArray().map(function (x) {
                data[x.name] = x.value;
            });
            //将data转为json字符串
            var jsonData = JSON.stringify(data);
            $.ajax({
                url:"/api/v1.0/sessions",
                type:"post",
                data: jsonData,
                contentType: "application/json",
                dataType: "json",
                headers:{
                    "X-CSRFTOKEN":getCookie("csrf_token")
                },
                success: function (data) {
                    if (data.errno==0) {
                        // 登录成功，跳转到主页
                        location.href = "/";
                        return;
                    }else {
                        // 其他错误信息，在页面中展示
                        $("#password-err span").html(data.errmsg);
                        $("#password-err").show();
                        return;
                    }
                }
            });
    })

})