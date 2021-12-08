
var upload = function(form) {
    const formData = new FormData(event.target);
    const fileInput = document.getElementById("file-input")
    const name = document.querySelector('input[name="type"]:checked').value;
    formData.append("file", fileInput.files[0]);
    formData.append("name", name)
    fetch('/v1/wallet/' + name, {
      method: "POST",
      body: formData
    });
}

var init = function() {
    form = document.getElementById("csv-upload");
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        upload(event);
    });
    uploadButton = document.getElementById("upload-button");

};

document.addEventListener("DOMContentLoaded", function(event) {
    init();
});