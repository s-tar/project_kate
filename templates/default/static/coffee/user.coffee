root = exports ? this

class User
  processing = false

  sendUserData = (sn, data, cb)->
    $.ajax
      type: "POST",
      url: root.base_url + "/user/login/"+sn,
      data: {
          data: JSON.stringify(data)
      },
      success: (data) ->
          if(data.status == 'ok')
              processing = false
              cb?.success?()

  login:
    fb:(cb) ->
      processing = if not processing then true else false
      FB.getLoginStatus (response) ->
        if response.status == 'connected'
          sendUserData('fb', response, cb)
        else
          FB.login((response) ->
            if response.authResponse
              sendUserData('fb', response, cb)
            else
              processing = false
              cb?.fail?() if typeof cb.fail is 'function'
              console.log('User cancelled login or did not fully authorize.');
          , {scope: 'email,user_likes'})
    vk: (cb) ->
      processing = if not processing then true else false
      VK.Auth.getLoginStatus (response) ->
        response.session = ''
        if response.session
          sendUserData('vk',response.session, cb)
        else
          VK.Auth.login (response) ->
            if response.session
              sendUserData('vk',response.session, cb)
            else
              processing = false
              cb?.fail?() if typeof cb.fail is 'function'

              console.log('User cancelled login or did not fully authorize.')

    native: (data) ->
      console.log(data)
      if data
        $.ajax
          type: "POST",
          url: root.base_url + "/user/login/native",
          data: {
              email: data.email,
              password: data.password
          },
          dataType: 'json',
          success: (data) ->
            window.location.reload()
#            socket.emit('user.login');
#            popup.hide();
#            widget.update("user.header");
  logout: ->
    $.ajax
      type: "POST",
      url: root.base_url + "/user/logout",
      data: {},
      dataType: 'json',
      success: (data) ->
        window.location.reload()

user = new User()
window.user = user

$(document).on 'click', '.user-registration',(e) ->
  e.preventDefault()
  self = $(this)
#  self.addClass('busy')
  widget.get 'user.registration.form',{}, (html) ->
#    self.removeClass('busy')
    root.popup.show({title: 'Регистрация', content: html, caller: self})


$(document).on 'click', '.user-login-native', (e)->
  e.preventDefault()
  self = $(this)
#  self.addClass('busy')
  widget.get 'user.login.form',{}, (html) ->
#    self.removeClass('busy')
    root.popup.show({title: 'Авторизация', content: html, caller: self})


$(document).on 'click', '.user-login-fb', ->
  self = $(this)
  self.addClass('busy')
  user.login.fb
    success: ->
      window.location.reload()
    fail: ->
      self.removeClass('busy')


$(document).on 'click', '.user-login-vk', ->
  self = $(this)
  self.addClass('busy')
  user.login.vk
    success: ->
      window.location.reload()
    fail: ->
      self.removeClass('busy')


$(document).on 'click', '.user-logout', ->
  user.logout()