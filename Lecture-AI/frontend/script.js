async function upload() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];
    const summaryEl = document.getElementById("summary");
    const questionsEl = document.getElementById("questions");
    const statusEl = document.getElementById("status");

    if (!file) {
        statusEl.innerText = "Please choose a PDF, MP3, or WAV file first.";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    statusEl.innerText = "Processing lecture...";
    summaryEl.innerText = "";
    questionsEl.innerText = "";

    try {
        const response = await fetch("http://127.0.0.1:5000/process", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong while processing the lecture.");
        }

        summaryEl.innerText = data.summary;
        questionsEl.innerText = data.questions;
        statusEl.innerText = "Lecture processed successfully.";
    } catch (error) {
        statusEl.innerText = error.message;
    }
}