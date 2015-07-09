/**
 * Created by mr.S on 21.11.14.
 */
$(document).ready(function(){
    $(".new-language, .language-list .item a").on("click", function(e){
        e.preventDefault();
        var data = {};
        var id = $(this).closest('.item').attr("item_id");
        var title = "Новый язык";
        if(!!id)  title = "Редактировать язык";
        data.id = id;
        widget.get("language.form", data, function(form){
            popup.show({
                title: title,
                html: form
            });
        });
    });

    $(document).on("submit", "form.language-form", function(e){
        var form = $(this);
        form.trigger("ajax_submit", function(response){
            if(response.status == 'ok') {
                window.location.reload()
            }else if(response.status == 'fail') {
                showErrors(form, response.errors);
            }
        })
        e.preventDefault();
        return false;
    });

    $(document).on("click", ".button.change-default", function(e){
        var item = $(this).closest('.item')
        var id = item.attr('item_id');
        var route = $(this).closest('.list, .icon-list').attr('route').replace(/\/+$/, '');
        var action = 'change_default'
        if(!!$(this).attr('action')) action = $(this).attr('action')
        var is_default = !item.hasClass('default');
        var _this = $(this);
        e.preventDefault();
            $.ajax({
                type: "POST",
                url: base_url + route + '/' + action,
                data: {id: id, is_default : is_default},
                dataType: 'json',
                success: function(data) {
                    if(data.status == "ok") {
                        _this.closest('.list, .icon-list').find('.item').removeClass("default");
                        if(data.is_default == true) item.addClass("default");
                    }else{
                        popup.show({
                            title: "Ошибка",
                            text: "Произошла ошибка..."
                        })
                    }
                }
            });
        });

});