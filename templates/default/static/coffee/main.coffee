root = exports ? this
root.base_url = location.protocol+'//'+location.hostname+(if location.port then ':'+location.port else '')

$(document).ready ->
  $.get("/config/sn", (config) ->
    FB.init({
      appId      : config.fb.app_id,
      status     : true,
      cookie     : true,
      xfbml      : true
    })

    VK.init({
      apiId: config.vk.app_id,
      onlyWidgets: true
    })
  )

  root.popup = new Popup()
  root.widget = new Widget()


$(window).load(->
  $('body').removeClass('transition-fix')
)
# ---------------------------------- POPUP -----------------------------------------
class Popup
  self = this
  _wrapper = $('.popup-wrapper')
  _background = _wrapper.find('.background')
  _popup = _wrapper.find('.popup')
  _title = _popup.find('.title .text')
  _close = _popup.find('.title .close')
  _content = _popup.find('.popup-content')
  last_caller = null

  last_caller_center = () ->
    top = 0
    left = 0
    if last_caller
      left = last_caller.offset().left + last_caller.outerWidth()/2 - _wrapper.width()/2
      top =last_caller.offset().top + last_caller.outerHeight()/2 - _wrapper.height()/2
    return {left: left, top: top}

  show: ({title,content, close, caller} = {}) ->
    close ?= true
    title ?= ''

    last_caller = caller
    caller_center = last_caller_center()

    _popup.css({
      'opacity': '0',
      '-webkit-transform' : 'translate(' + caller_center.left + 'px,'+ caller_center.top + 'px) scale(0)',
      '-moz-transform'    : 'translate(' + caller_center.left + 'px,'+ caller_center.top + 'px) scale(0)',
      '-ms-transform'     : 'translate(' + caller_center.left + 'px,'+ caller_center.top + 'px) scale(0)',
      '-o-transform'      : 'translate(' + caller_center.left + 'px,'+ caller_center.top + 'px) scale(0)',
      'transform'         : 'translate(' + caller_center.left + 'px,'+ caller_center.top + 'px) scale(0)',
    });


    if close then _close.show() else _close.hide()
    _title.html(title)
    _content.html(content)
    root.apply_plugins(_content)
    _wrapper.show()

    setTimeout(->
      _background.addClass('visible')
      _popup.css({
        'opacity': '1',
        '-webkit-transform' : '',
        '-moz-transform'    : '',
        '-ms-transform'     : '',
        '-o-transform'      : '',
        'transform'         : '',
      })
    , 1)

  hide: (direction, scale) ->
    d = last_caller_center()
    if not scale then scale = 0
    switch direction
      when "bottom" then d = {left: 0, top: _wrapper.height()/2}
      when "top" then d = {left: 0, top: -_wrapper.height()/2}
      when "left" then d = {left: -_wrapper.width()/2, top: 0}
      when "right" then d = {left: _wrapper.width()/2, top: 0}

    _popup.css({
      'opacity': '0',
      '-webkit-transform' : 'translate(' + d.left + 'px,'+ d.top + 'px) scale('+ scale+')',
      '-moz-transform'    : 'translate(' + d.left + 'px,'+ d.top + 'px) scale('+ scale+')',
      '-ms-transform'     : 'translate(' + d.left + 'px,'+ d.top + 'px) scale('+ scale+')',
      '-o-transform'      : 'translate(' + d.left + 'px,'+ d.top + 'px) scale('+ scale+')',
      'transform'         : 'translate(' + d.left + 'px,'+ d.top + 'px) scale('+ scale+')'
    });
    _background.removeClass('visible')
    setTimeout(->
      _wrapper.hide()
    , 400)

$(document).on 'click', '.popup-wrapper .title .close',->
  root.popup.hide()
# -------------------------------- WIDGET -----------------------------------------
class Widget
  update: (name, cb) ->
    widget = if typeof name == 'string' then $('div[widget="'+name+'"]') else name;
    attr = {}
    $(widget[0].attributes).each(->
      attr[this.nodeName] = this.value
    )
    if(widget.length)
      $.ajax
        type: "POST",
        url: root.base_url + "/widget/"+widget.attr('widget'),
        data: attr,
        dataType: 'html',
        success: (data) ->
          widget.html(data)
          cb() if typeof cb is 'function'

  get: (name, attr,  cb) ->
    $.ajax
      type: "POST",
      url: base_url + "/widget/"+name,
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify({"data": attr}),
      dataType: 'html',
      success: (html) ->
          cb(html) if typeof cb is 'function'


root.apply_plugins = (content) ->
  content.find('.image-loader').ImageLoader()