function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var imageCodeId = "";

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

// 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
function generateImageCode() {
    var cur_image_id = generateUUID();
    var imageCodeUrl = "/api/v1.0/imagecode?pre="+imageCodeId+"&cur="+cur_image_id;
    $(".image-code>img").attr("src",imageCodeUrl);
    imageCodeId=cur_image_id;
}
// function generateImageCode() {
//     // 获取图片验证码
//     // 生成验证码编号 uuid
//     var cur_image_id = generateUUID();
//     // 将uuid拼接成url设置到html页面中
//     var url = "/api/v1.0/image_code?pre=" + imageCodeId + "&cur=" + cur_image_id;
//     $(".image-code>img").attr("src", url);
//     imageCodeId =cur_image_id ;
// }

// 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
// function generateImageCode() {
//     // 生成一个编号
//     // 严格一点的使用uuid保证编号唯一， 不是很严谨的情况下，也可以使用时间戳
//     imageCodeId = generateUUID();
//
//     // 设置页面中图片验证码img标签的src属性
//     var imageCodeUrl = "/api/v1.0/imagecode/" + imageCodeId;
//     $(".image-code>img").attr("src", imageCodeUrl);
//}

function sendSMSCode() {
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    } 
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    // $.get("/api/v1.0/smscode/"+mobile, { text:imageCode, id:imageCodeId},
    //     function(data){
    //         if (0 != data.errno) {
    //             $("#image-code-err span").html(data.errmsg);
    //             $("#image-code-err").show();
    //             if (2 == data.errno || 3 == data.errno) {
    //                 generateImageCode();
    //             }
    //             $(".phonecode-a").attr("onclick", "sendSMSCode();");
    //         }
    //         else {
    //             var $time = $(".phonecode-a");
    //             var duration = 60;
    //             var intervalid = setInterval(function(){
    //                 $time.html(duration + "秒");
    //                 if(duration === 1){
    //                     clearInterval(intervalid);
    //                     $time.html('获取验证码');
    //                     $(".phonecode-a").attr("onclick", "sendSMSCode();");
    //                 }
    //                 duration = duration - 1;
    //             }, 1000, 60);
    //         }
    // }, 'json');
    var data = {mobile:mobile,text:imageCode,id:imageCodeId};
    $.ajax({
        url:"/api/v1.0/smscode",
        method:"POST",
        headers:{
            "X-CSRFToken":getCookie("csrf_token")
        },
        data:JSON.stringify(data),
        contentType:"application/json",
        dataType:"json",
        success:function (rep) {
            // alert(rep.errno);
            if (rep.errno=="0"){
                var $time = $(".phonecode-a");
                var duration = 60;
                var intervalid = setInterval(function(){
                    duration = duration - 1;
                    $time.html(duration + "秒");
                    if(duration == 1){
                        clearInterval(intervalid);
                        $time.html('获取验证码');
                        $(".phonecode-a").attr("onclick", "sendSMSCode();");
                    }

                },1000,60)
            }else {
                $("#phone-code-err span").html(rep.errmsg);
                $("#phone-code-err").show();
                $(".phonecode-a").attr("onclick","sendSMSCode();");
                if (rep.errno == "4004"){
                    generateImageCode()
                }
            }

        }
    })
}

$(document).ready(function() {
    generateImageCode();
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });

    //给表单田间自定义的提交行为
    $(".form-register").submit(function(e){
        //阻止表单的默认行为
        e.preventDefault();
        mobile = $("#mobile").val();
        phoneCode = $("#phonecode").val();
        passwd = $("#password").val();
        passwd2 = $("#password2").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!phoneCode) {
            $("#phone-code-err span").html("请填写短信验证码！");
            $("#phone-code-err").show();
            return;
        }
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        if (passwd != passwd2) {
            $("#password2-err span").html("两次密码不一致!");
            $("#password2-err").show();
            return;
        }
        //向后端发送请求，提交用户注册信息
        var req_data={
            mobile:mobile,
            sms_code:phoneCode,
            password:passwd
        };
        //将js对象转换为json字符串
        req_json = JSON.stringify(req_data);
        // $.post("/api/v1_0/users", req_json, function (resp) {
        //     if (resp.errno == 0) {
        //         // 注册成功, 引导到主页页面
        //         location.href = "/";
        //     } else {
        //         alert(resp.errmsg);
        //     }
        // })
        $.ajax({
            url:"/api/v1.0/users",//请求路径url
            type:"post",//请求方式
            data:req_json,//发送的请求数据ｖ
            contentType:"application/json",//指明向后端发送的是json格式数据
            dataType:"json",//指明从后端受到的数据ｖ是Ｊson数据ｖ
            headers:{
                "X-CSRFToken": getCookie("csrf_token")
            },
            success:function (resp) {
                if (resp.errno == 0) {
                    // 注册成功, 引导到主页页面
                    location.href = "/";
                }else{
                    alert(resp.errmsg);
                    $("#password2-err span").html(resp.errmsg);
                    $("#password2-err").show()
                }
            }


        })
    });
})