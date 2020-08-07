// Connect to io socket
var socket = io().connect('http://localhost:5000');

// Get the input and description
const fileInput = document.querySelector('#upload-files input[type=file]');
const description = document.querySelector('#upload-files .file-name');

// Get the current window location
var current = window.location.pathname;

fileInput.onchange = () => {
  $(".progress-bar").text("0%");
  $(".progress-bar").attr("value", 0);
  if (fileInput.files.length > 0) {
    $(".progress-bar").show();
    description.textContent = "Uploading Files..";
    var formData = new FormData();
    var bookname = "NULL";
    // Relay the folder name
    var foldername = fileInput.files[0]['webkitRelativePath'].split("/")[0].split(" ").join("_");
    var uploadpath = '/upload/' + foldername;
    document.getElementById('upload-form').action = uploadpath;
    for (var i = 0; i < fileInput.files.length; i++) {
      // Check whether we are uploading for aeneas or dp2
      var filename = fileInput.files[i].name;
      if (filename.includes("html") && filename !== "ncc.html") {
        // Relay the book name if aeneas
        var bookname = fileInput.files[i].name.split(".")[0];
      }
      formData.append('uploads', fileInput.files[i]);
    }
    $.ajax({
      url: uploadpath,
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      xhr: function () {
        var xhr = new XMLHttpRequest();

        xhr.upload.addEventListener("progress", function (evt) {
          if (evt.lengthComputable) {
            var percentComplete = evt.loaded / evt.total;
            $(".file-input").attr("disabled", true);
            percentComplete = parseInt(percentComplete * 100);

            $(".progress-bar").text(percentComplete + "%");
            $(".progress-bar").attr("value", percentComplete);

            if (percentComplete === 100) {
              if (current === "/") {
                description.textContent = "Aeneas Processing..";
              } else {
                description.textContent = "Converting to epub3..";
              }
              $("#upload-files").attr("class", "file is-centered is-boxed is-info has-name is-large");
              $("#file-label-span").text("Upload Complete");
              //console.log("upload completed, " + percentComplete + "%");
              // Let server know that its uploaded and that the client expects data
              // Emit Uploaded for Aeneas Uploaded_Convert for Conversion to Epub3
              if (current === "/") {
                socket.emit('uploaded', foldername, bookname);
              } else {
                socket.emit('uploaded_convert', foldername, bookname);
              }
              $("#process-feed").show();
            }
          }
        }, false);
        return xhr;
      }
    });
  }
}

socket.on('newdata', (d) => {
  //console.log(d);
  $("#process-feed").show();
  $("#process-feed").prepend(d);
});

socket.on('refresh', () => {
  description.textContent = "Processing Complete, Refreshing..";
  setTimeout(() => { location.reload(); }, 2000);
});

socket.on('error', () => {
  if (current === "/") {
    description.textContent = "Aeneas Processing Error";
  }
  else {
    description.textContent = "Conversion Processing Error";
  }
  $("#upload-files").attr("class", "file is-centered is-boxed is-danger has-name is-large");
  $("#process-feed").attr("class", "textarea is-large is-danger has-fixed-size");
});