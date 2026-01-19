// ======================
// GLOBAL ELEMENTS
// ======================
const processBtn = document.getElementById("processBtn");
const statusDiv = document.getElementById("status");
const resultsDiv = document.getElementById("results");
const summaryStore = {};

// ======================
// TOKEN HELPERS
// ======================
function getToken() {
    return localStorage.getItem("token");
}

function isLoggedIn() {
    return !!getToken();
}

// ======================
// INIT (LOGIN / LOGOUT)
// ======================
document.addEventListener("DOMContentLoaded", () => {
    const loginBtn = document.getElementById("loginBtn");
    const logoutBtn = document.getElementById("logoutBtn");

    loginBtn.onclick = async () => {
        const email = document.getElementById("username").value.trim();
        if (!email) {
            alert("Enter email");
            return;
        }

        const res = await fetch("http://127.0.0.1:8000/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email })
        });

        const data = await res.json();
        localStorage.setItem("token", data.access_token);

        alert("Logged in!");
        updateAuthUI();
    };

    logoutBtn.onclick = () => {
        localStorage.removeItem("token");
        alert("Logged out");
        updateAuthUI();
    };

    updateAuthUI();
});

function updateAuthUI() {
    const loginBtn = document.getElementById("loginBtn");
    const logoutBtn = document.getElementById("logoutBtn");

    if (isLoggedIn()) {
        loginBtn.style.display = "none";
        logoutBtn.style.display = "inline-block";
    } else {
        loginBtn.style.display = "inline-block";
        logoutBtn.style.display = "none";
    }
}

// ======================
// PROCESS PODCAST
// ======================
processBtn.onclick = async () => {
    const token = getToken();
    if (!token) {
        alert("Please login first");
        return;
    }

    const fileInput = document.getElementById("audioFile");
    if (!fileInput.files.length) {
        alert("Please select an audio file");
        return;
    }

    // UI LOCK
    processBtn.disabled = true;
    processBtn.innerText = "Processing...";
    statusDiv.innerText = "Uploading podcast...";
    resultsDiv.style.display = "none";
    document.getElementById("loader").style.display = "block";

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("title", fileInput.files[0].name);

    try {
        console.log("Uploading with token:", token);

        const response = await fetch(
            "http://127.0.0.1:8000/pipeline/upload",
            {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`
                },
                body: formData
            }
        );

        if (!response.ok) {
            throw new Error("Upload failed");
        }

        const data = await response.json();
        statusDiv.innerText =
            "Podcast uploaded. Processing started.\nPodcast ID: " +
            data.podcast_id;

        pollStatus(data.podcast_id);

    } catch (err) {
        alert("Upload failed");
        console.error(err);
        resetUI();
    }
};

// ======================
// POLL STATUS
// ======================
async function pollStatus(podcastId) {
    statusDiv.innerText = "Processing podcast...";

    const interval = setInterval(async () => {
        try {
            const res = await fetch(
                `http://127.0.0.1:8000/pipeline/status/${podcastId}`,
                {
                    headers: {
                        Authorization: "Bearer " + getToken()
                    }
                }
            );

            const data = await res.json();

            if (data.status === "completed") {
                clearInterval(interval);
                showResults(data);
            }
        } catch (e) {
            console.error("Polling error", e);
        }
    }, 4000);
}

// ======================
// SHOW RESULTS
// ======================
function showResults(data) {
    document.getElementById("loader").style.display = "none";
    processBtn.disabled = false;
    processBtn.innerText = "Process Podcast";

    statusDiv.innerText = "Processing completed ✅";

    const pdfUrl =
        "http://127.0.0.1:8000/" +
        data.pdf_path.replace(/\\/g, "/");

    resultsDiv.style.display = "block";
    resultsDiv.innerHTML = `
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

// ======================
// HISTORY
// ======================
document.getElementById("historyBtn").onclick = async () => {
    const historyDiv = document.getElementById("history");
    historyDiv.innerHTML = "Loading history...";

    const res = await fetch(
        "http://127.0.0.1:8000/pipeline/my-podcasts",
        {
            headers: {
                Authorization: "Bearer " + getToken()
            }
        }
    );

    const data = await res.json();

    data.forEach(p => {
        if (p.summary) summaryStore[p.id] = p.summary;
    });

    historyDiv.innerHTML = `
        <h3>My Podcasts</h3>
        ${data.map(p => `
            <div class="card">
                <strong>${p.title}</strong><br/>
                Status: ${p.status}<br/>

                ${p.status === "completed"
            ? `
                            <button onclick="showSummary(${p.id})">
                                📝 View Summary
                            </button>
                            <a href="http://127.0.0.1:8000/${p.pdf_path.replace(/\\/g, "/")}" target="_blank">
                                📄 PDF
                            </a>
                            <button onclick="deletePodcast(${p.id})">
                                🗑 Delete
                            </button>
                          `
            : "⏳ Processing..."
        }
            </div>
        `).join("")}
    `;
};

// ======================
// MODAL
// ======================
function showSummary(podcastId) {
    const summary = summaryStore[podcastId];
    if (!summary) {
        alert("Summary not available yet.");
        return;
    }
    document.getElementById("modalSummary").innerText = summary;
    document.getElementById("summaryModal").style.display = "block";
}

document.getElementById("closeModal").onclick = () => {
    document.getElementById("summaryModal").style.display = "none";
};

// ======================
// DELETE
// ======================
async function deletePodcast(id) {
    if (!confirm("Delete this podcast?")) return;

    await fetch(
        `http://127.0.0.1:8000/pipeline/delete/${id}`,
        {
            method: "DELETE",
            headers: {
                Authorization: "Bearer " + getToken()
            }
        }
    );

    document.getElementById("historyBtn").click();
}

// ======================
// UI RESET
// ======================
function resetUI() {
    processBtn.disabled = false;
    processBtn.innerText = "Process Podcast";
    document.getElementById("loader").style.display = "none";
}