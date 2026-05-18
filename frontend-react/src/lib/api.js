const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "https://voltrax123-podc-backend.hf.space").replace(/\/$/, "");

async function parseError(response) {
  const text = await response.text();
  try {
    const data = JSON.parse(text);
    return data.detail || data.message || text;
  } catch {
    return text || response.statusText;
  }
}

function networkErrorMessage(error) {
  return [
    `Could not reach the backend at ${API_BASE_URL}.`,
    "Check that FastAPI is running and did not restart during processing.",
    "If you use uvicorn --reload, restart the backend after this update so runtime media writes happen outside the watched project folder.",
    `Original browser error: ${error.message}`,
  ].join(" ");
}

let modelsRequest = null;

export async function fetchModels() {
  if (modelsRequest) {
    return modelsRequest;
  }

  modelsRequest = fetch(`${API_BASE_URL}/models`)
    .then(async (response) => {
      if (!response.ok) {
        throw new Error(await parseError(response));
      }
      return response.json();
    })
    .catch((error) => {
      modelsRequest = null;
      throw error;
    });

  return modelsRequest;
}

export async function fetchModelsUncached() {
  const response = await fetch(`${API_BASE_URL}/models`);
  if (!response.ok) {
    throw new Error(await parseError(response));
  }
  return response.json();
}

export async function processPodcast(file) {
  const formData = new FormData();
  formData.append("file", file);

  let response;
  try {
    response = await fetch(`${API_BASE_URL}/process`, {
      method: "POST",
      body: formData,
    });
  } catch (error) {
    throw new Error(networkErrorMessage(error));
  }

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}

export async function askPodcast(question) {
  const params = new URLSearchParams({ question });
  const response = await fetch(`${API_BASE_URL}/ask?${params.toString()}`);

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}

export async function downloadPdf() {
  const response = await fetch(`${API_BASE_URL}/download-pdf`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.blob();
}

export { API_BASE_URL };
