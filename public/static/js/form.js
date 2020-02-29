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
        body.value = JSON.stringify(editor.getContents());

        console.log("Submitted", $(form).serialize(), $(form).serializeArray());
        $(form).submit();
    };


    $('input[wtype="date"]').bootstrapMaterialDatePicker({
        time: false,
        format : 'DD.MM.YYYY',
        nowButton : true,
        lang: 'ru',
        minDate : new Date(),
    });
});