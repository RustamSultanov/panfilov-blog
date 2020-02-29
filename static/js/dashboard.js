$(function() {
    $('#dropzone-files').dropzone({
        parallelUploads: 10,
        maxFilesize:     50000,
        filesizeBase:    1000,
        addRemoveLinks:  true,
    });
    $('#dropzone-docs').dropzone({
        parallelUploads: 10,
        maxFilesize:     50000,
        filesizeBase:    1000,
        addRemoveLinks:  true,
    });
    $('#dropzone-invoices').dropzone({
        parallelUploads: 10,
        maxFilesize:     50000,
        filesizeBase:    1000,
        addRemoveLinks:  true,
    });

    // Mock the file upload progress (only for the demo)
    //
    Dropzone.prototype.uploadFiles = function(files) {
        var minSteps         = 6;
        var maxSteps         = 60;
        var timeBetweenSteps = 100;
        var bytesPerStep     = 100000;
        var isUploadSuccess  = Math.round(Math.random());

        var self = this;

        for (var i = 0; i < files.length; i++) {

            var file = files[i];
            var totalSteps = Math.round(Math.min(maxSteps, Math.max(minSteps, file.size / bytesPerStep)));

            for (var step = 0; step < totalSteps; step++) {
                var duration = timeBetweenSteps * (step + 1);

                setTimeout(function(file, totalSteps, step) {
                    return function() {
                        file.upload = {
                            progress: 100 * (step + 1) / totalSteps,
                            total: file.size,
                            bytesSent: (step + 1) * file.size / totalSteps
                        };

                        self.emit('uploadprogress', file, file.upload.progress, file.upload.bytesSent);
                        if (file.upload.progress == 100) {

                            if (isUploadSuccess) {
                                file.status =  Dropzone.SUCCESS;
                                self.emit('success', file, 'success', null);
                            } else {
                                file.status =  Dropzone.ERROR;
                                self.emit('error', file, 'Ошибка загрузки', null);
                            }

                            self.emit('complete', file);
                            self.processQueue();
                        }
                    };
                }(file, totalSteps, step), duration);
            }
        }
    };
});


function load_tasks(element){           
    event.preventDefault();
    element.siblings('a').removeClass('active');
    element.addClass('active');
    $('#tasks_manager').load(element[0].href)
    $('a')[0].focus()
    return false;
}
function load_request(element){
    event.preventDefault();
    element.siblings('a').removeClass('active');
    element.addClass('active');
    $('#request_manager').load(element[0].href)
    $('a')[0].focus()
    return false;
}
function load_feedback(element){
    event.preventDefault();
    element.siblings('a').removeClass('active');
    element.addClass('active');
    $('#feedback_manager').load(element[0].href)
    $('a')[0].focus()
    return false;
}

function load_ideas(element){
    event.preventDefault();
    element.siblings('a').removeClass('active');
    element.addClass('active');
    $('#ideas_manager').load(element[0].href)
    $('a')[0].focus()
    return false;
}
