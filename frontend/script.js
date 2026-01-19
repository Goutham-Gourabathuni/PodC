const processBtn = document.getElementById("processBtn");
const statusDiv = document.getElementById("status");
const resultsDiv = document.getElementById("results");
const summariesDiv = document.getElementById("summaries");

processBtn.onclick = async () => {
    const fileInput = document.getElementById("audioFile");
    if (!fileInput.files.length) {
        alert("Please select an audio file");
        return;
    }

    processBtn.disabled = true;
    processBtn.innerText = "Processing...";

    statusDiv.innerText = "Uploading podcast and starting processing...";
    resultsDiv.style.display = "none";

    document.getElementById("loader").style.display = "block";

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("title", fileInput.files[0].name);

    const response = await fetch("http://127.0.0.1:8000/pipeline/upload", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    pollStatus(data.podcast_id);

    statusDiv.innerText =
        "Podcast uploaded successfully. Processing in background.\nPodcast ID: " +
        data.podcast_id;
};

async function pollStatus(podcastId) {
    const statusDiv = document.getElementById("status");
    const resultDiv = document.getElementById("results");

    statusDiv.innerText = "Processing podcast...";

    const interval = setInterval(async () => {
        const res = await fetch(
            `http://127.0.0.1:8000/pipeline/status/${podcastId}`
        );
        const data = await res.json();

        if (data.status === "completed") {
            clearInterval(interval);

            statusDiv.innerText = "Processing completed ✅";

            document.getElementById("loader").style.display = "none";

            processBtn.disabled = false;
            processBtn.innerText = "Process Podcast";

            // Normalize Windows path → URL path
            const pdfUrl =
                "http://127.0.0.1:8000/" +
                data.pdf_path.replace(/\\/g, "/");

            resultDiv.style.display = "block";
            resultDiv.innerHTML = `
                <div class="card">
                    <h3>📝 Summary</h3>
                    <p>${data.summary}</p>

                    <h3>🏷 Topics</h3>
                    <ul>
                    ${data.topics.map(t => `<li>${t}</li>`).join("")}
                    </ul>

                    <a href="${pdfUrl}" target="_blank" download class="btn">
                    📄 Download PDF
                    </a>
                </div>
                `;
        }
    }, 4000);
}
