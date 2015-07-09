/**
 * Created by mr.S on 18.09.14.
 */
$(document).on('change', '#upload input[type=file]', function(e){
    var form = $(this).closest('form');
    var formData = new FormData(form[0]);
    var url = form.attr("action");
    var method = form.attr("method");

    $.ajax({
        url: url,
        type: method,
        data: formData,
        async: false,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            if(response.status == "ok"){
                var win = $('.mce-window');
                var inputs = win.find('input');
                inputs.eq(0)[0].value = base_url+response.url;
                inputs.eq(2)[0].value = response.width;
                inputs.eq(3)[0].value = response.height;
            }
            if(response.status == "fail"){
            }
        }
    });
    e.preventDefault();
    return false;
});
$(document).ready(function(){
    var processing = false;
    if(typeof(tinymce) != "undefined")
        tinymce.init({
            selector: ".editor",
            plugins: [
                "pagebreak",
                "advlist autolink lists link image charmap print preview anchor",
                "searchreplace visualblocks code fullscreen",
                "insertdatetime media table contextmenu paste"
            ],
            pagebreak_separator: "<!-- page break -->",
            file_browser_callback: function(field_name, url, type, win) {
                $('#upload input').click();
            },
            paste_data_images: true,
            setup: function (editor) {
                editor.on('change', function () {
                    tinymce.triggerSave();
                });
            },
            toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image"
        });
});
$(document).on("click", "input.submit, button.submit", function(){
    if($(this).attr('processing') == "true")return;
    $(this).attr('processing', "true");
    $('body').addClass('loading');
    $(this).closest("form").submit();
});

$(document).on("submit", "form.ajax", function(e){
    e.preventDefault();
});

$(document).on("ajax_submit", "form", function(e, cb){
    var formData = new FormData($(this)[0]);
    var url = $(this).attr("action");
    var method = $(this).attr("method");
    var _this = $(this);
    $('body').addClass('loading');

    $.ajax({
        url: url,
        type: method,
        data: formData,
        async: false,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            if(response.status == "fail"){
                _this.find(".submit").attr("processing", "");
            }
            if(typeof(cb) == 'function')cb(response);
            $('body').removeClass('loading');
        }
    });
    e.preventDefault();
    return false;
});

$(document).on("submit", "form.ajax_submit, form.ajax-submit", function(e){
var form = $(this);
form.trigger("ajax_submit", function(response){
    if(response.status == 'ok') {
        if(!!response.redirect)
            window.location.href=response.redirect
        else if(!!response.reload)
            window.location.reload()
    }else if(response.status == 'fail') {
        showErrors(form, response.errors);
        $('body').removeClass('loading');
    }
})
e.preventDefault();
return false;
});
function showErrors(form , errors) {
    $(form).find(".error").remove();
    for(key in errors){
        if (errors.hasOwnProperty(key)) {
            $(form).find("[name='"+key+"']").each(function(i){
                if(!!errors[key][i]){
                    var error = $('<span class="error"><div class="text">'+errors[key][i][0]['message']+'</div></span>');
                    $(this).after(error);
                    error.css("display", "block")
                    var text = error.find(".text");
                    if(error.find(".text").outerWidth() > $(this).outerWidth()){
                        text.css("white-space", "normal");
                        text.outerWidth($(this).outerWidth());
                    }
                    error.css("display", "none")
                    $(this).change(function(){
                        error.fadeOut();
                    })
                    $(this).focus(function(){
                        error.css('opacity','0.3')
                    });
                    $(this).blur(function(){
                        error.css('opacity','')
                    })
                    error.fadeIn();
                }

            });

        }
    }
}


//$(document).on('keydown', 'textarea.autoresize', function (e){
//    $(this).css("height","");
//    var height = $(this).height();
//    if(e.which == 13) {
//        $(this).css("padding-top",'1.145em')
//    }
//    var fontSize = $(this).css('font-size');
//    var lineHeight = Math.floor(parseInt(fontSize.replace('px','')) * 1.5);
//    var new_height = this.scrollHeight - lineHeight;
//    new_height = (new_height > height) ? new_height : height;
//    $(this).height(new_height);
//});
//
//
//$(document).on('keyup', 'textarea.autoresize', function (e){
//    $(this).css("height","");
//    var height = $(this).height();
//    var maxheight = parseInt($(this).css('max-height').replace("px", ""));
//
//    if(e.which == 13) {
//        $(this).css("padding-top",'')
//    }
//    var fontSize = $(this).css('font-size');
//    var lineHeight = Math.floor(parseInt(fontSize.replace('px','')) * 1.5);
//    var new_height = this.scrollHeight - lineHeight;
//    new_height = (new_height > height) ? new_height : height;
//    $(this).height(new_height);
//    if(new_height > maxheight)
//        $(this).css('overflow-y', 'scroll');
//    else
//        $(this).css('overflow-y', '');
//    popup.center();
//});

$(document).on('keydown keyup change', 'input, textarea', function (e){
    $(this).removeClass('has-value');
    if($(this).val() != "")
        $(this).addClass('has-value');
});

function preview(input, cb) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            if(typeof(cb) == "function") cb(e.target.result)
        }

        reader.readAsDataURL(input.files[0]);
    }
}
$(document).on("change", ".image-loader input[type=file]", function(){
    var container = $(this).closest(".image-loader");
    container.addClass("loading");
    if($(this).val() == ''){
        container.removeClass("loading");
        container.removeClass("has-image");
        container.find(".source").css("background-image", "none");
    } else {

        preview(this, function(src){
            container.removeClass("loading");
            container.addClass("has-image");
            container.find(".source").css("background-image", "url('"+src+"')");
        });
    }
});

var image_multiloader = {
    update_order: function(container){
        var order = 1
        container.find('.item:not(.unsortable)').each(function(){
            $(this).find('input.order').val(order);
            order++;
        })
    }
}
$(document).ready(function(){
    $(".image-multiloader.sortable").sortable({
        items:  '.item:not(.unsortable)',
        update: function(e, ui){
            image_multiloader.update_order($(this))
        }
    });
})
$(document).on("mouseenter", ".image-multiloader .item:not(.new)", function(e){
    $(this).find(".buttons").stop( true, true ).slideDown();
});
$(document).on("mouseleave", ".image-multiloader .item", function(e){
    $(this).find(".buttons").stop( true, false ).slideUp();
});

$(document).on('change', '.image-multiloader .item input[type=file]',function(){
    var item = $(this).closest(".item");
    var _this = this
    if(item.hasClass('new')){
        var n = item.clone();
        item.before(n);
        item.removeClass('new');
        item.removeClass('unsortable');
        var mt = parseInt(item.css("marginTop").replace('px',''));
        item.css("marginTop", item.height()/2+mt+"px");
        item.find('input[name=action]').val("new");
        item.hide();

        item.addClass("loading");
        preview(_this, function(src){
            item.closest('.sortable').sortable('refresh');
            item.removeClass("loading");
            item.find(".source").css("background-image", "url('"+src+"')");
            image_multiloader.update_order(item.closest('.image-multiloader'))
            item.animate({
                height:'toggle',
                width:'toggle',
                padding:'toggle',
                marginTop: mt}, 350,function(){});
        });
    }else{
        item.addClass("loading");
        if($(this).val() == ''){
            item.removeClass("loading");
            //item.removeClass("has-image");
            //item.find(".source").css("background-image", "none");
        }else{
            preview(_this, function(src){
                item.find('input[name=action]').val("edit");
                item.removeClass("loading");
                item.removeClass("new");
                item.find(".source").css("background-image", "url('"+src+"')");
            });
        }
    }

})

$(document).on('click', '.image-multiloader .item .button.delete-image',function(){
    var item = $(this).closest(".item");
    var mt = parseInt(item.css("marginTop").replace('px',''));
    mt =  item.height()/2+mt+"px"
    item.find('input[name=action]').val("delete");
    item.find('input[type=file]').val("");
    item.animate({
        height:'toggle',
        width:'toggle',
        padding:'toggle',
        marginTop: mt},350);
});

$(document).on('click', '.image-multiloader .item .button.change-visibility',function(){
    var item = $(this).closest(".item");
    item.toggleClass('invisible')
    item.find('.visible').val(item.hasClass('invisible') ? 0 : 1);
});

$(document).on('click', '.dropdown-list > .current', function(){
    var dropdown = $(this).parent();
    var list = dropdown.find('.list')
    list.stop(true).slideToggle();
});

$(document).on('focus', 'textarea.autosize',  function(){
    autosize($(this));
});

$(document).on('mouseover', '.field-wrapper', function(e){
    $(this).find('.field-edit-buttons').stop().animate({'opacity': 1}, 500);
});

$(document).on('mouseout', '.field-wrapper', function(e){
    $(this).find('.field-edit-buttons').stop().animate({'opacity': 0}, 500);
});