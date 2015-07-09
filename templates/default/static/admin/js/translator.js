$(document).on('click', '.translator-tabs .tab:not(.is-active)', function(){
    var container = $(this).closest('.translator-tabs');
    var code = $(this).attr('code');
    var _this = $(this)
    $.post('/admin/translator/change_translation_language',{'code': code})
        .success(function(){
            window.location.reload();
//            container.find('.tab').removeClass('is-active');
//            _this.addClass('is-active');
        })
})

$(document).on('click', '.translator-language-selector .item.current', function(){
    var container = $(this).closest('.translator-language-selector');
    container.find('.languages-list').stop().slideToggle()
})

$(document).on('click', '.translator-language-selector .languages-list .item', function(){
    var code = $(this).attr('code');
    var _this = $(this)
    $.post('/admin/translator/change_language',{'code': code})
        .success(function(){
            window.location.reload();
        })
})

$(document).on("click", ".dictionary-list .item", function(){
    var data = {}
    var id = $(this).closest('.item').attr("item_id");
    var title = "Редактировать информацию"
    data.id = id
    widget.get("dictionary.form", data, function(form){
        popup.show({
            title: title,
            html: form
        });
    });
});

$(document).on("submit", "form.dictionary-form", function(e){
    var form = $(this);
    form.trigger("ajax_submit", function(response){
        if(response.status == 'ok') {
            var id = response.dictionary.id
            $('.item[item_id='+id+'] .text').text(response.dictionary.text);
            popup.hide()
        }else if(response.status == 'fail') {
            showErrors(form, response.errors);
        }
    })
    e.preventDefault();
    return false;
});