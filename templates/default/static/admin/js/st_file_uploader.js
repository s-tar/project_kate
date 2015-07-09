/**
 * Created by mr.S on 04.01.15.
 */
var stFileUpload = {};
stFileUpload.files = {};
(function($) {
    var __name__ = "st-file-uploader";
    var _this = this;
    var methods = {
        init : function(options) {
            this.each(function() {
                $(this).addClass(__name__);
                var loader = $('<input type="file" multiple/>').addClass(__name__+'-loader').hide();
                var files = $(this).find('.files').addClass(__name__+'-files');
                var placeholder = $(this).find('.placeholder').addClass(__name__+'-placeholder');
                var uploaded_files = {};
                if(files.length == 0) { files = $('<div></div>').addClass(__name__+'-files'); $(this).append(files);}

                $(this).append(loader);
                files.find('.file').each(function(i){
                    var item = createItem($(this).attr('data-src'), $(this).attr('data-id'), $(this).attr('data-visible'));
                    files.append(item);
                    $(this).remove();

                });

                $(this).on('dragenter', function (e) {
                    e.stopPropagation();
                    e.preventDefault();
                });
                $(this).on('dragover', function (e) {
                    e.stopPropagation();
                    e.preventDefault();
                });
                $(this).on('dragleave', function (e) {
                    e.stopPropagation();
                    e.preventDefault();
                });
                $(this).on('drop', function (e) {
                    e.preventDefault();
                    var uFiles = e.originalEvent.dataTransfer.files;
                     for (var i = 0; i < uFiles.length; i++)  {
                        addItem(uFiles[i], files);
                     }
                });

                files.sortable({
                    items:  '.'+__name__+'-file',
                    update: function(e, ui){
                        updateOrder();
                    }
                });
                $(".sortable").disableSelection();
                $(this).closest('form').on('submit', function(e, cb){
                    if($(this).attr('processing'))return;
                    $(this).attr('processing','processing');
                    var formData = new FormData($(this)[0]);
                    var url = $(this).attr("action");
                    var method = $(this).attr("method");
                    var _this = $(this);
                    $(this).find('.'+__name__+'-file').each(function(){
                        formData.append('file', uploaded_files[$(this).attr('data-file')]);
                    });
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
                                $(this).attr('processing','');
                            }
                            if(typeof(cb) == 'function')cb(response);
                        }
                    });
                    e.preventDefault();
                    return false;
                });

                placeholder.on('click', function(){ loader.trigger('click')});
                loader.change(function() {
                    var uFiles = $(this).get(0).files;

                    for (var i = 0; i < uFiles.length; ++i) {
                        addItem(uFiles[i], files);
                    }
                    loader.val('');
                });


                function addItem(file, container) {
                    var item = createItem('','','1','new', container.find('.'+__name__+'-file:not(.deleted)').length+1);
                    var reader = new FileReader();

                    if(file instanceof File) {
                        item.find('input[type=file]').val(file.name);
                        var id = 'file_'+(Object.keys(uploaded_files).length+1);
                        item.attr('data-file', id);
                        uploaded_files[id] = file;
                    }
                    reader.onload = function(e) {
                        setItemImage(item, e.target.result);
                    }
                    container.append(item);
                    reader.readAsDataURL(file);
                }
            });
        },
        destroy: function(){
            this.each(function(){

            });
        }
    };

    function createItem(src, id, visible, action, order){
        var item = $('<div></div>').addClass(__name__+'-file');
        var buttons = $('<div></div>').addClass('buttons');
        var icon = $('<div></div>').addClass('icon');
        item.attr('data-id', id || '');
        item.append($('<input type="hidden" name="file.id" />').val(id || ''));
        item.append($('<input type="hidden" name="file.visible" />').val(visible || ''));
        item.append($('<input type="hidden" name="file.action" />').val(action || ''));
        item.append($('<input type="hidden" name="file.order" />').val(order || '0'));
        item.append($('<input type="file" name="file"/>').val());
        buttons.append($('<div></div>').addClass('button change-visibility fa '));
        buttons.append($('<div></div>').addClass('button delete fa'));
        item.append(icon);
        item.append(buttons);
        if(visible === '0') item.addClass('invisible');
        setItemImage(item, src);
        return item;
    }

    function updateOrder(){
        var files = $('.'+__name__+'-files');
        files.find('.'+__name__+'-file:not(.deleted)').each(function(i){
            var order = $(this).find("input[name='file.order']");
            if(order.val() != i+1 || order.val() == '') {
                order.val(i+1);
                var action = $(this).find("input[name='file.action']");
                if(action.val() == '') action.val('edit');
            }
        });
    }

    function setItemImage(item ,src) {
        item.find('.icon').css('background-image', 'url(\''+(src || '')+'\')');
    }

    function handleFileUpload(files,obj) {
       for (var i = 0; i < files.length; i++)  {
           addItem(files[i], files);
            var fd = new FormData();
            fd.append('file', files[i]);

            status.setFileNameSize(files[i].name,files[i].size);
            sendFileToServer(fd,status);

       }
    }

    $(document).on('click', '.'+__name__+' .delete', function(){
        var item = $(this).closest('.'+__name__+'-file');
        var height = item.outerHeight(true);
        item.find('.buttons').stop(true).slideUp(function(){$(this).remove();});
        item.animate({'margin-top': height/2, 'width': 0, 'height': 0}, function(){
            $(this).css('display','none');
            $(this).find('[name="file.action"]').val('delete');
            item.addClass('deleted');
            if(!item.attr('data-id'))item.remove();
            updateOrder();
            if(item.closest('.'+__name__+'-files').find('.'+__name__+'-file:not(.deleted)').length == 0)
                item.closest('.'+__name__).find('.'+__name__+'-placeholder').show();
        });

    });

    $(document).on('click', '.'+__name__+' .change-visibility', function(){
        var item = $(this).closest('.'+__name__+'-file');
        var height = item.outerHeight(true);
        item.toggleClass('invisible');
        item.find('input[name="file.visible"]').val(item.hasClass('invisible') ? 0 : 1);
        item.find('input[name="file.action"]').val('edit');
        updateOrder();
    });

    $(document).on('mouseenter', '.'+__name__+'-file', function(){
        $(this).find('.buttons').stop(true, true).slideDown();
    });

    $(document).on('mouseleave', '.'+__name__+'-file', function(){
        $(this).find('.buttons').stop(true, false).slideUp();
    });

    $(document).on('dragenter', function (e) {
        e.stopPropagation();
        e.preventDefault();
    });

    $(document).on('dragover', function (e) {
      e.stopPropagation();
      e.preventDefault();
    });

    $(document).on('drop', function (e){
        e.stopPropagation();
        e.preventDefault();
    });

    $.fn.stFileUploder = function(methodOrOptions) {
        if ( methods[methodOrOptions] ) {
            return methods[ methodOrOptions ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof methodOrOptions === 'object' || ! methodOrOptions ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  methodOrOptions + ' does not exist on jQuery.tooltip' );
        }
    };
})(jQuery)
