async function upload() {
    let file = document.getElementById("fileInput").files[0];

    let formData = new FormData();
    formData.append("file", file);

    let response = await fetch("http://127.0.0.1:5000/process", {
        method: "POST",
        body: formData
    });

    let data = await response.json();

    document.getElementById("summary").innerText = data.summary;
    document.getElementById("questions").innerText = data.questions;
}