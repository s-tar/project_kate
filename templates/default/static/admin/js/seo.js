/**
 * Created by mr.S on 21.10.14.
 */

$(document).on('keydown', '.seo-save .new textarea', function(e){
    if(!e.which)return;
    var parent = $(this).parent();
    var clone = parent.clone();
    parent.removeClass("new");
    clone.css('display', 'none');
    clone.find('.error').remove();
    parent.find('.delete').css('display','block')
    parent.find('textarea[name=seot_text]').addClass('deletable');
    parent.after(clone)
    clone.slideDown();
    clone.keydown();
})
$(document).on('keydown keyup', '.seo-save textarea', function(e){
    var parent = $(this).parent();
    parent.find('.delete').height($(this).height()+8);
})
$(document).on("submit", "form.seo-save", function(e){
    var form = $(this);
    form.trigger("ajax_submit", function(response){
        if(response.status == 'ok') {
            window.location.href="/admin/seo"
        }else if(response.status == 'fail') {
            showErrors(form, response.errors);
        }
    })
    e.preventDefault();
    return false;
});

$(document).on('click', '.seo-save .delete', function(e){
    var parent = $(this).parent();
    parent.slideUp(function(){
        parent.find('textarea[name=seot_text]').val("");
    })
})

$(document).on("click", ".seo-delete", function(e){
        var _this = $(this);
        e.preventDefault();
        popup.show({
            title: "Удаление ссылки",
            text: "Вы уверены, что хотите удалить ссылку?",
            buttons: [
                {
                    caption: "Да",
                    left: true,
                    action: function(){
                        $.ajax({
                            type: "POST",
                            url: base_url + "/admin/seo/delete/"+_this.attr("iid"),
                            data: {},
                            dataType: 'json',
                            success: function(data) {
                                if(data.status == "ok") {
                                    _this.closest(".item").slideUp(function(){
                                        $(this).remove();
                                    });
                                    popup.hide()
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