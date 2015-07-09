/**
 * Created by mr.S on 04.09.14.
 */
user = {}
user.processing = false;
user.login = function() {
    function sendUserData(sn, data){
        $.ajax({
            type: "POST",
            url: base_url + "/user/login/"+sn,
            data: {
                data: JSON.stringify(data)
            },
            success: function(data) {
                if(data.status == 'ok') {
                    widget.update("user.header");
                    user.processing = false;
                }
            }
        });
    }

    function vk() {
        if(!user.processing){user.processing = true;}else{return false}
        VK.Auth.getLoginStatus(function(response) {
            response.session = ''; // force VK.Auth.login
            if (response.session) {
                sendUserData('vk',response.session);
            } else {
                VK.Auth.login(function(response) {
                    if (response.session) {
                        sendUserData('vk',response.session);
                    } else {
                        user.processing = false;
                        console.log('User cancelled login or did not fully authorize.');
                    }
                });
            }
        });
    }

    function fb() {
        if(!user.processing){user.processing = true;}else{return false}
        FB.getLoginStatus(function(response) {
            if (response.status === 'connected') {
                sendUserData('fb',response);
            } else {
                FB.login(function(response) {
                    if (response.authResponse) {
                        sendUserData('fb',response);
                    } else {
                        user.processing = false;
                        console.log('User cancelled login or did not fully authorize.');
                    }
                }, {scope: 'email,user_likes'});
            }
        });
    }

    function native(data){
        if(!data) {
            widget.get('user.login.form',{}, function(html){
                popup.show({title: 'Авторизация', content: html, close: false});
            });
        } else {
            $.ajax({
                type: "POST",
                url: base_url + "/user/login/native",
                data: {
                    email: data.email,
                    password: data.password
                },
                dataType: 'json',
                success: function(data) {
                    widget.update("user.header");
                }
            });
        }

    }

    return {
        processing: user.processing,
        vk: vk,
        fb: fb,
        native: native
    }
}();

user.logout = function(){
    $.ajax({
        type: "POST",
        url: base_url + "/user/logout",
        data: {},
        dataType: 'json',
        success: function(data) {
            //widget.update("user.header");
            window.location.href = '/';
        }
    });
}

$(document).on('submit', '.user-login-form', function(e){
    var form = $(this);
    form.trigger("ajax_submit", function(response){
        if(response.status == 'ok') {
            window.location.reload();
        }else if(response.status == 'fail') {
            showErrors(form, response.errors);
        }
    })
    e.preventDefault();
    return false;
});
