root = exports ? this

$(document).on("submit", "form.processing", (e) ->
  e.preventDefault()
)

$(document).on("submit", "form.ajax", (e) ->
  e.preventDefault()
)

$(document).on("ajax-submit", "form", (e, cb) ->
  if $(this).hasClass('processing') then return false
  $(this).addClass('processing')
  formData = new FormData($(this)[0])
  url = $(this).attr("action")
  method = $(this).attr("method")
  $this = $(this)
  $('body').addClass('loading')
  $.ajax({
    url: url,
    type: method,
    data: formData,
    async: false,
    cache: false,
    contentType: false,
    processData: false,
    success: (response) ->
      if response.status == "fail" then $this.removeClass("processing")
      if typeof(cb) == 'function' then  cb(response, $this)
      $('body').removeClass('loading')
  });
  e.preventDefault()
  return false
)

$(document).on("submit", "form.ajax-submit", (e) ->
  form = $(this)
  form.trigger("ajax-submit", (response, form) ->
    if response.status == 'ok'
      if !!response.redirect
        window.location.href = response.redirect
      else if !!response.reload
        window.location.reload()
    else if response.status == 'fail'
      showErrors(form, response.errors)
      form.removeClass("processing")
      $('body').removeClass('loading')
  )
  e.preventDefault()
  return false
)


root.showErrors = (form , errors) ->
  $(form).find(".error").remove();
  console.log errors
  for key, val of errors
    if errors.hasOwnProperty(key)
      $(form).find("[name='"+key+"']").each( (i) ->
        if !!errors[key][i]
          error = $('<span class="error"><div class="text">'+val[i][0]['message']+'</div></span>')
          $(this).after(error);
          error.css("display", "block")
          text = error.find(".text")
          if error.find(".text").outerWidth() > $(this).outerWidth()
            text.css("white-space", "normal")
            text.outerWidth($(this).outerWidth())
          error.css("display", "")
          error.css("opacity", "1")
          $(this).change ()-> error.fadeOut()
          $(this).focus ()-> error.css('opacity','0')
          $(this).blur ()-> error.css('opacity','1')
      )


# -------------------------------------- IMAGE LOADER ------------------------------
root.preview = (input, cb) ->
  if (input.files && input.files[0])
    reader = new FileReader()
    reader.onload = (e) ->
      if(typeof(cb) == "function")
        cb(e.target.result)
    reader.readAsDataURL(input.files[0]);


(($, window) ->
  class ImageLoader

    defaults:
      image: ''

    constructor: (el, options) ->
      @options = $.extend({}, @defaults, options)
      @$el = $(el)
      @$el.wrap($('<div></div>').addClass('image-loader-wrapper'))
      wrapper = @$el.parent()
      wrapper.attr('name', $(el).attr('name')+'_wrapper')
      if $(el).attr('data-title')
        $(el).after($('<div></div>').addClass('image-loader-title').html($(el).attr('data-title')))

      $(el).on('change', ->
        if $(this).val()
          wrapper.addClass('loading')
        root.preview($(this)[0], (image) ->
          wrapper.css('background-image', "url('"+image+"')")
          wrapper.removeClass('loading')
          wrapper.addClass('has-image')
        )
      )

  $.fn.extend ImageLoader: (option, args...) ->
    @each ->
      $this = $(this)
      data = $this.data('ImageLoader')

      if !data
        $this.data 'ImageLoader', (data = new ImageLoader(this, option))
      if typeof option == 'string'
        data[option].apply(data, args)

) window.jQuery, window
# ----------------------------------------------------------------------------------