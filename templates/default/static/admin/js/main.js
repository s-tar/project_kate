/**
 * Created by mr.S on 04.09.14.
 */

var base_url = location.protocol+'//'+location.hostname+(location.port ? ':'+location.port: '');
//var base_url = 'http://192.168.1.2:3000';

widget = {}
widget.update = function(name){
    var widget = $('div[widget="'+name+'"]');
    var attr = {}
    $(widget[0].attributes).each(function() {
        attr[this.nodeName] = this.value;
    });
    if(widget.length)
        $.ajax({
            type: "POST",
            url: base_url + "/widget/"+name,
            data: attr,
            dataType: 'html',
            success: function(data) {
                widget.fadeOut(function(){
                    widget.html(data);
                    widget.fadeIn();
                });

            }
        });
}
widget.get = function(name, attr,  cb){
    $.ajax({
        type: "POST",
        url: base_url + "/widget/"+name,
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({"data": attr}),
        dataType: 'html',
        success: function(html) {
            cb(html);
        }
    });
}

popup = {}
popup.show = function(options) {
    var popup = $(".main-popup")
    var container = popup.find(".container");
    var content = popup.find(".popup-content");
    popup.find(".popup-header").removeClass('non-close');
    if(!!options.title) popup.find(".popup-header .text").html(options.title);
    if(!!options.text) content.html('<div class="text">'+options.text+'</div>');
    if(!!options.html) content.html(options.html);
    if(options.close === false)
        popup.find(".popup-header").addClass('non-close');

    if(!!options.buttons){
        var btn_container = $('<div class="buttons"></div>');
        var left = $('<div class="buttons-left"></div>');
        var right = $('<div class="buttons-right"></div>');
        btn_container.append(left);
        btn_container.append(right);
        for(var i in options.buttons) {
            (function(index) {
                var b = options.buttons[index];
                var button = $('<input type="button" value="'+ b.caption+'"/>');
                if(typeof(b.action) == 'function'){
                    button.on("click", function(){
                        if($(this).attr('processing') == 'true') return;
                        $(this).attr('processing', 'true')
                        b.action();
                    });
                }
                if(b.left == true) left.append(button); else right.append(button);
            })(i);
        }
        content.append(btn_container);
    }

    popup.css("display","block");
    popup.css("visibility","hidden");
    container.css("margin-left", -container.width()/2);
    container.css("margin-top", -container.height()/2);
    popup.css("display","none");
    popup.css("visibility","");
    popup.fadeIn();

}
popup.hide = function(cb) {
    var popup = $(".main-popup")
    var _cb = function(){}
    if(typeof(cb) == 'function') _cb = cb
    popup.fadeOut(_cb)
}

function preview(input, cb) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            if(typeof(cb) == "function") cb(e.target.result)
        }

        reader.readAsDataURL(input.files[0]);
    }
}
(function($){
    $.fn.disableSelection = function() {
        return this
                 .attr('unselectable', 'on')
                 .css('user-select', 'none')
                 .on('selectstart', false);
    };
})(jQuery);

$(document).on('mouseenter', ".list .item:not(.new)", function(){
    $(this).find(".edit-buttons").stop( true, true ).fadeTo( 300, 1 );
})

$(document).on('mouseleave', ".list .item", function(){
    $(this).find(".edit-buttons").stop( true, true ).fadeTo( 300, 0 );
})

$(document).on("mouseenter", ".icon-list .item:not(.new)", function(e){
    $(this).find(".buttons").stop( true, true ).slideDown();
});
$(document).on("mouseleave", ".icon-list .item", function(e){
    $(this).find(".buttons").stop( true, false ).slideUp();
});


$(document).on("click", "tr.item[href] td:not(.buttons)", function(){
    window.location.href = $(this).closest(".item").attr("href");
})

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
        })
    }
})

$(document).on('click', '.item .change-visibility', function(e){
    var item = $(this).closest('.item')
    var id = item.attr('item_id');
    var route = $(this).closest('.list, .icon-list').attr('route');
    if(!!route) route = route.replace(/\/+$/, '');
    var action = 'change_visibility'
    if(!!$(this).attr('action')) action = $(this).attr('action')
    var visible = item.hasClass('invisible');
    var _this = $(this);
    if(!!route) {
        route = route.replace(/\/+$/, '');
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: base_url + route + '/' + action,
            data: {id: id, visible : visible},
            dataType: 'json',
            success: function(data) {
                if(data.status == "ok") {
                    item.removeClass("invisible");
                    if(data.visible == false) item.addClass("invisible");
                }else{
                    popup.show({
                        title: "Ошибка",
                        text: "Произошла ошибка..."
                    })
                }
            }
        });
    }
});

$(document).on("click",".item .button.delete", function(e){
    var _this = $(this);
    var item = $(this).closest('.item')
    var list = $(this).closest('.list, .icon-list')
    var id = item.attr('item_id');
    var route = list.attr('route').replace(/\/+$/, '');
    var action = 'delete'
    if(!!$(this).attr('action')) action = $(this).attr('action')
    e.preventDefault();
    popup.show({
        title: "Удаление",
        text: "Вы подтверждаете удаление?",
        buttons: [
            {
                caption: "Да",
                left: true,
                action: function(){
                    $.ajax({
                        type: "POST",
                        url: base_url + route + "/" + action,
                        data: {id: id},
                        dataType: 'json',
                        success: function(data) {
                            if(data.status == "ok") {
                                var mt = parseInt(item.css("marginTop").replace('px',''));
                                mt =  item.height()/2+mt+"px"


                                popup.hide(function(){
                                    if(list.hasClass('list')) {
                                        item.animate({
                                            height:'toggle'},350, function(){
                                                item.remove();
                                        });
                                    }else if(list.hasClass('icon-list')) {
                                        item.animate({
                                            height:'toggle',
                                            width:'toggle',
                                            marginTop: mt},350, function(){
                                                item.remove();
                                        });
                                    }else{
                                        item.remove();
                                    }
                                })
                            }else{
                                popup.show({
                                    title: "Ошибка",
                                    text: "Произошла ошибка при удалении..."
                                })
                            }
                        }
                    });
                }
            },
            {
                caption: "Нет",
                action: function(){popup.hide()}
            }
        ]
    });
});

$(document).ready(function(){
    $(".list.sortable, .icon-list.sortable").sortable({
        items:  '.item:not(.unsortable)',
        update: function(e, ui){
            var order = []
            var route = $(this).attr('route').replace(/\/+$/, '');
            $(this).find(".item:not(.new)").each(function(){
                order.push($(this).attr("item_id"))
            });

            $.ajax({
                type: "POST",
                url: base_url + route + "/change_order",
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify({order : order}),
                dataType: 'json',
                success: function(data) {
                    if(data.status == "ok") {

                    }else{
                        popup.show({
                            title: "Ошибка",
                            text: "Произошла ошибка..."
                        })
                    }
                }
            });
        }
    });
    $(".sortable").disableSelection();
})
$(document).ready(function(){
    $('.calendar').each(function(){
        var data = {lang: 'ru',
            closeOnDateSelect: true}
        if($(this).hasClass('date'))
            data.timepicker = false;
        if(!!$(this).attr('format')) data.format = $(this).attr('format');
        $(this).datetimepicker(data);
    });

});

$(document).ready(function(){
    $('.file-uploader').stFileUploder();
});
/* ------------------------------------- TRAINING ------------------------------------------------------- */
$(document).on('click', '.training-form .new-question', function(e){
    var q_tmp = $('.training-form .question.template');
    var q = q_tmp.clone();
    var n = $('.training-form .question').length;
    q.prepend('<input type="hidden" name="num" value="'+n+'"/>');
    q.removeClass('template');
    q.attr('data-num', n);
    q.find('textarea[name=question]').attr('name', 'question['+n+']');
    q.find('input[name=qid]').attr('name', 'qid['+n+']');
    q.find('input[name=qaction]').attr('name', 'qaction['+n+']');
    q.find('input[name=aid]').attr('name', 'aid['+n+']');
    q.find('input[name=answer]').attr('name', 'answer['+n+']');
    q.find('input[name=aaction]').attr('name', 'aaction['+n+']');
    q.find('input[name=is_true]').attr('name', 'is_true['+n+']');
    q.hide();
    q_tmp.after(q);
    q.slideDown();
    e.preventDefault();
    return false;
});
$(document).on('click', '.training-form .new-answer', function(e){
    var li_tmp = $(this).parent().find('li').last();
    var li = li_tmp.clone();
    li.removeClass('true');
    li.find('input').val('');
    li.find('input.action').val('new');
    li.find('input.is_true').val('0');
    li.find('.error').remove();
    li.hide()
    li_tmp.after(li);
    var question = li.closest('.question');
    var num = question.find('input[name=num]').val();
    var qaction = question.find('input[name="qaction['+num+']"]');
    if(qaction.val() == '') qaction.val('edit');
    li.slideDown();
    e.preventDefault();
    return false;
});

$(document).on('change', '.question li input', function(){
    var action = $(this).closest('li').find('.action');
    if(action.val() == '') {
        action.val('edit');
        $(this).closest('.question').find('.qaction').val('edit');
    }
});

$(document).on('change', '.question .qtext', function(){
    var action = $(this).closest('.question').find('.qaction');
    if(action.val() == '')action.val('edit');
});

$(document).on('click', '.training-form .question ul > .field-wrapper .delete', function(e){
    var question = $(this).closest('.question');
    var action = question.find('.qaction');
    if(action.val() != 'new') action.val('delete');
    question.slideUp(function(){ if(action.val() == 'new') question.remove();});
});

$(document).on('click', '.training-form .question ul li .delete', function(e){
    var answer = $(this).closest('li');
    var qaction = answer.closest('.question').find('.qaction');
    var action = answer.find('.action');
    if(qaction.val() == '')answer.closest('.question').find('.qaction').val('edit');
    if(action.val() != 'new') action.val('delete');
    answer.slideUp(function(){ if(action.val() == 'new') answer.remove(); });
});

$(document).on('click', '.training-form .question ul li .field-edit-buttons .is-true', function(e){
    var true_answer = $(this).closest('ul').find('li.true');
    var true_answer_action = true_answer.find('.action');
    true_answer.removeClass('true');
    true_answer.find('.is_true').val(0);
    if(true_answer_action.val() == '') true_answer_action.val('edit');

    var answer = $(this).closest('li');
    var qaction = answer.closest('.question').find('.qaction');
    var action = answer.find('.action');
    answer.find('.is_true').val(1);
    answer.addClass('true');
    if(qaction.val() == '')answer.closest('.question').find('.qaction').val('edit');
    if(action.val() == '') action.val('edit');
});
/* ------------------------------------- -------- ------------------------------------------------------- */
$(document).on('click', 'form.about-save .submit-button', function(e){
    var form = $(this).closest('form');
    $('body').addClass('loading');
    setTimeout(function(){
        form.trigger("submit", function(response){
            if(response.status == 'ok') {
                window.location.reload();
            }else if(response.status == 'fail') {
                $('body').removeClass('loading');
                showErrors(form, response.errors);
            }
        })
    }, 1000);

    e.preventDefault();
    return false;
});