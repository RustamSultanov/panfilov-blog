$(function() {
    $('#dropzone-files').dropzone({
        parallelUploads: 10,
        maxFilesize:     50000,
        filesizeBase:    3000,
        addRemoveLinks:  true,
        success : function(file, response){
            console.log(this.emit);
            console.log(response);
        }        
    });

    // Mock the file upload progress (only for the demo)
    //
Dropzone.options.myAwesomeDropzone = {
    maxFilesize: 5,
    addRemoveLinks: true,
    dictResponseError: 'Server not Configured',
  };

});