/**
 * Created by mr.S on 10.10.14.
 */


$(document).ready(function(){
    $(document).on('keydown', '.contacts-save .new input[name=address],' +
        '.contacts-save .new input[name=email],' +
        '.contacts-save .new input[name=phone_num],' +
        '.contacts-save .new input[name=phone_description]', function(){
        var container = $(this).parent();
        var new_field = container.clone();
        new_field.css('display', 'none');
        container.removeClass('new');
        new_field.find('input:not([type=button])').val('');
        container.after(new_field);
        new_field.slideDown();
    });

    $(document).on('submit', '.contacts-save', function(e){
        $(this).find('.new').remove()
        var form = $(this);
        form.trigger("ajax_submit", function(response){
            window.location.reload();
        })
        e.preventDefault();
        return false;
    });

    $(document).on('click', '.contacts-save .button.cancel', function(e){
        window.location.reload();
    });

    $(document).on('click', '.contacts-save input.delete', function(e){
        var container = $(this).parent();
        container.slideUp(function(){
            container.find('input[type=text]').val('<delete>');
        });
    });
});