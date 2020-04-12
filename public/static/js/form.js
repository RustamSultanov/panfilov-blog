$(function() {
    if (!window.Quill) {
        return $('#quill-editor,#quill-toolbar').remove();
    }

    var editor = new Quill('#quill-editor', {
        modules: {
            toolbar: '#quill-toolbar'
        },
        placeholder: 'Type something',
        theme: 'snow'
    });


    var form = document.querySelector('form');
    form.onsubmit = function() {
        // Populate hidden form on submit
        var body = document.querySelector('input[name=body]');
        var content = document.querySelector('input[name=content]');
        body.value = $('div.ql-editor').html();
        content.value = $('div.ql-editor').html();

        console.log("Submitted", $(form).serialize(), $(form).serializeArray());

        // No back end to actually submit to!
        //alert('Для production варианта нужно изменить функцию сабмита формы!')
        //return false;
    };

    var okText = "Ок";
    var clearText = "Очистить";
    var nowText = "Сейчас";
    var cancelText = "Отменить";

    $('#b-m-dtp-date').bootstrapMaterialDatePicker({
        weekStart: 1,
        time: false,
        format: 'DD.MM.YYYY',
        okText: okText,
        clearText: clearText,
        nowText: nowText,
        cancelText: cancelText,
        lang: 'ru',
        clearButton: true
    });

    $('#b-m-dtp-datetime').bootstrapMaterialDatePicker({
        weekStart: 1,
        format : 'DD MMMM YYYY - HH:mm',
        shortTime: true,
        nowButton : true,
        okText: okText,
        clearText: clearText,
        nowText: nowText,
        cancelText: cancelText,
        lang: 'ru',
        minDate : new Date()
    });

    $('#b-m-dtp-time').bootstrapMaterialDatePicker({
        date: false,
        shortTime: false,
        okText: okText,
        clearText: clearText,
        nowText: nowText,
        cancelText: cancelText,
        lang: 'ru',
        format: 'HH:mm'
    });

    $('.select2').each(function() {
        $(this)
            .wrap('<div class="position-relative"></div>')
            .select2({
                placeholder: 'Выберите значение',
                dropdownParent: $(this).parent()
            });
    });

});