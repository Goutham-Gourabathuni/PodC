import React, { useEffect, useMemo, useRef, useState } from "react";
import {
  AlertCircle,
  CheckCircle2,
  Download,
  FileAudio,
  FileText,
  HelpCircle,
  Loader2,
  Moon,
  Sparkles,
  UploadCloud,
} from "lucide-react";
import { askPodcast, downloadPdf, fetchModels, processPodcast } from "./lib/api";

const allowedTypes = ["audio/mpeg", "audio/mp3", "audio/wav", "audio/x-wav", "audio/mp4", "audio/x-m4a"];
const allowedExtensions = [".mp3", ".wav", ".m4a"];

function formatSeconds(value) {
  if (value === undefined || value === null || Number.isNaN(Number(value))) {
    return "0s";
  }

  const total = Math.max(0, Math.round(Number(value)));
  const minutes = Math.floor(total / 60);
  const seconds = total % 60;
  return minutes > 0 ? `${minutes}m ${seconds.toString().padStart(2, "0")}s` : `${seconds}s`;
}

function isAllowedAudio(file) {
  const extension = file.name.slice(file.name.lastIndexOf(".")).toLowerCase();
  return allowedTypes.includes(file.type) || allowedExtensions.includes(extension);
}

function StatusBanner({ type = "info", children }) {
  const styles = {
    info: "border-blue-400/20 bg-blue-500/15 text-blue-700 dark:text-blue-300",
    success: "border-emerald-400/20 bg-emerald-500/15 text-emerald-700 dark:text-emerald-300",
    error: "border-rose-400/20 bg-rose-500/15 text-rose-700 dark:text-rose-300",
  };

  const Icon = type === "success" ? CheckCircle2 : type === "error" ? AlertCircle : FileText;

  return (
    <div className={`flex gap-3 rounded-lg border px-5 py-4 text-base leading-7 ${styles[type]}`}>
      <Icon className="mt-1 h-5 w-5 flex-none" aria-hidden="true" />
      <div>{children}</div>
    </div>
  );
}

function App() {
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem("podc-theme") === "dark";
  });
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [processed, setProcessed] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processError, setProcessError] = useState("");
  const [pdfState, setPdfState] = useState({ loading: false, error: "", ready: false });
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [askState, setAskState] = useState({ loading: false, error: "" });
  const [reviewed, setReviewed] = useState({});
  const [models, setModels] = useState(null);
  const fileInputRef = useRef(null);
  const processingRef = useRef(false);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
    localStorage.setItem("podc-theme", darkMode ? "dark" : "light");
  }, [darkMode]);

  useEffect(() => {
    fetchModels()
      .then(setModels)
      .catch(() => setModels(null));
  }, []);

  const topics = useMemo(() => (Array.isArray(data?.topics) ? data.topics : []), [data]);

  function selectFile(nextFile) {
    if (!nextFile) {
      return;
    }

    if (!isAllowedAudio(nextFile)) {
      setProcessError("Please upload an MP3, WAV, or M4A podcast audio file.");
      return;
    }

    setFile(nextFile);
    setProcessError("");
    setPdfState({ loading: false, error: "", ready: false });
  }

  async function handleProcess() {
    if (!file || isProcessing || processingRef.current) {
      return;
    }

    processingRef.current = true;
    setIsProcessing(true);
    setProcessError("");
    setAnswer("");
    setQuestion("");
    setReviewed({});

    try {
      const result = await processPodcast(file);
      setData(result);
      setProcessed(true);
    } catch (error) {
      setData(null);
      setProcessed(false);
      setProcessError(`Backend error while processing podcast: ${error.message}`);
    } finally {
      processingRef.current = false;
      setIsProcessing(false);
    }
  }

  async function handleDownloadPdf() {
    setPdfState({ loading: true, error: "", ready: false });

    try {
      const blob = await downloadPdf();
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = "podc_summary.pdf";
      anchor.click();
      URL.revokeObjectURL(url);
      setPdfState({ loading: false, error: "", ready: true });
    } catch (error) {
      setPdfState({ loading: false, error: error.message, ready: false });
    }
  }

  async function handleAsk(event) {
    event.preventDefault();
    const trimmed = question.trim();

    if (!trimmed || askState.loading) {
      return;
    }

    setAskState({ loading: true, error: "" });
    setAnswer("");

    try {
      const result = await askPodcast(trimmed);
      setAnswer(result.answer || "No answer");
    } catch (error) {
      setAskState({ loading: false, error: error.message });
      return;
    }

    setAskState({ loading: false, error: "" });
  }

  return (
    <main className="min-h-screen bg-white text-slate-950 transition-colors duration-300 dark:bg-[#0e1117] dark:text-white">
      <div className="mx-auto flex w-full max-w-[880px] flex-col px-5 py-10 sm:px-8 sm:py-14">
        <div className="mb-20 flex items-center">
          <button
            type="button"
            aria-pressed={darkMode}
            onClick={() => setDarkMode((value) => !value)}
            className="group inline-flex items-center gap-3 text-base font-semibold text-slate-700 outline-none transition hover:text-slate-950 focus-visible:ring-2 focus-visible:ring-blue-500 dark:text-white dark:hover:text-white"
          >
            <span
              className={`relative h-5 w-10 rounded-full transition ${darkMode ? "bg-[#ff4b4b]" : "bg-slate-200"}`}
              aria-hidden="true"
            >
              <span
                className={`absolute top-1/2 h-4 w-4 -translate-y-1/2 rounded-full bg-white transition ${
                  darkMode ? "left-[21px]" : "left-1"
                }`}
              />
            </span>
            <Moon className="h-5 w-5 text-amber-400" aria-hidden="true" />
            Dark Mode
          </button>
        </div>

        <header className="mb-20 text-center">
          <h1 className="font-display text-[5.25rem] leading-none tracking-normal text-slate-950 dark:text-white sm:text-8xl">
            PodC
          </h1>
          <p className="mt-6 text-2xl font-medium text-slate-700 dark:text-slate-300 sm:text-[1.75rem]">
            The Automated Podcast Analyzer
          </p>
        </header>

        <section className="border-y border-slate-200 py-10 dark:border-white/20">
          <label className="mb-3 block text-base font-bold" htmlFor="podcast-file">
            Upload a podcast audio file
          </label>

          <div
            onDragOver={(event) => {
              event.preventDefault();
              setIsDragging(true);
            }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={(event) => {
              event.preventDefault();
              setIsDragging(false);
              selectFile(event.dataTransfer.files?.[0]);
            }}
            className={`flex flex-col gap-4 rounded-lg border px-5 py-4 transition sm:flex-row sm:items-center sm:justify-between ${
              isDragging
                ? "border-blue-400 bg-blue-500/10"
                : "border-slate-300 bg-slate-100 dark:border-transparent dark:bg-[#262730]"
            }`}
          >
            <div className="flex min-w-0 items-center gap-4">
              <UploadCloud className="h-9 w-9 flex-none text-slate-500 dark:text-slate-300" aria-hidden="true" />
              <div className="min-w-0">
                <p className="truncate text-lg font-bold">
                  {file ? file.name : "Drag and drop file here"}
                </p>
                <p className="mt-1 text-sm font-medium text-slate-500 dark:text-slate-300">
                  Limit 200MB per file • MP3, WAV, M4A
                </p>
              </div>
            </div>

            <input
              id="podcast-file"
              ref={fileInputRef}
              type="file"
              accept=".mp3,.wav,.m4a,audio/*"
              className="sr-only"
              onChange={(event) => selectFile(event.target.files?.[0])}
            />

            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="rounded-lg border border-slate-400/40 bg-slate-950 px-4 py-3 text-base font-semibold text-white transition hover:bg-slate-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 dark:bg-[#111827] dark:hover:bg-slate-800"
            >
              Browse files
            </button>
          </div>

          {file && (
            <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex min-w-0 items-center gap-2 text-sm font-medium text-slate-600 dark:text-slate-300">
                <FileAudio className="h-4 w-4 flex-none" aria-hidden="true" />
                <span className="truncate">{(file.size / (1024 * 1024)).toFixed(2)} MB selected</span>
              </div>

              <button
                type="button"
                onClick={handleProcess}
                disabled={isProcessing}
                className="inline-flex items-center justify-center gap-2 rounded-lg bg-[#111827] px-5 py-3 text-base font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {isProcessing ? <Loader2 className="h-5 w-5 animate-spin" /> : <Sparkles className="h-5 w-5" />}
                {isProcessing ? "Processing podcast..." : "Process Podcast"}
              </button>
            </div>
          )}

          <div className="mt-6 space-y-4">
            {processError && <StatusBanner type="error">{processError}</StatusBanner>}
            {processed && <StatusBanner type="success">Podcast processed successfully!</StatusBanner>}
            <StatusBanner>
              These topics and summaries are AI-generated. Please review them for accuracy before relying on them.
            </StatusBanner>
          </div>
        </section>

        {data?.episode_summary && (
          <section className="border-b border-slate-200 py-10 dark:border-white/20">
            <h2 className="mb-4 text-3xl font-bold">Episode Summary</h2>
            <p className="whitespace-pre-line text-lg leading-8 text-slate-700 dark:text-slate-200">{data.episode_summary}</p>
          </section>
        )}

        {topics.length > 0 && (
          <section className="border-b border-slate-200 py-10 dark:border-white/20">
            <h2 className="mb-8 text-3xl font-bold">Topics</h2>
            <div className="space-y-8">
              {topics.map((topic, index) => {
                const topicKey = topic.id || index + 1;

                return (
                  <article key={topicKey} className="space-y-3">
                    <h3 className="text-2xl font-bold">
                      Topic {index + 1}: {topic.title || "Untitled"}
                    </h3>
                    {topic.text && <p className="text-base leading-7 text-slate-700 dark:text-slate-200">{topic.text}</p>}
                    {topic.summary && (
                      <p className="text-sm leading-6 text-slate-500 dark:text-slate-300">
                        <span className="font-bold">Summary:</span> {topic.summary}
                      </p>
                    )}
                    <div className="flex flex-wrap items-center gap-3 text-sm font-medium text-slate-500 dark:text-slate-300">
                      <span>{formatSeconds(topic.start)} to {formatSeconds(topic.end)}</span>
                      {topic.confidence && (
                        <span className="rounded-full border border-slate-300 px-3 py-1 capitalize dark:border-white/20">
                          {topic.confidence} confidence
                        </span>
                      )}
                    </div>
                    <label className="inline-flex items-center gap-3 text-sm font-semibold">
                      <input
                        type="checkbox"
                        checked={Boolean(reviewed[topicKey])}
                        onChange={(event) =>
                          setReviewed((current) => ({ ...current, [topicKey]: event.target.checked }))
                        }
                        className="h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                      />
                      Mark Topic {index + 1} as reviewed
                    </label>
                    {reviewed[topicKey] && (
                      <p className="text-sm font-medium text-emerald-700 dark:text-emerald-300">Reviewed by human</p>
                    )}
                  </article>
                );
              })}
            </div>
          </section>
        )}

        {processed && (
          <section className="border-b border-slate-200 py-10 dark:border-white/20">
            <button
              type="button"
              onClick={handleDownloadPdf}
              disabled={pdfState.loading}
              className="inline-flex items-center justify-center gap-2 rounded-lg bg-[#111827] px-5 py-3 text-base font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {pdfState.loading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Download className="h-5 w-5" />}
              {pdfState.loading ? "Preparing PDF..." : "Download Summary as PDF"}
            </button>
            <div className="mt-4 space-y-3">
              {pdfState.ready && <StatusBanner type="success">PDF download is ready.</StatusBanner>}
              {pdfState.error && <StatusBanner type="error">Failed to generate PDF: {pdfState.error}</StatusBanner>}
            </div>
          </section>
        )}

        <section className="py-10">
          <div className="mb-6 flex items-center gap-4">
            <HelpCircle className="h-9 w-9 text-rose-500" aria-hidden="true" />
            <h2 className="text-3xl font-bold">Ask a question about the podcast</h2>
          </div>

          <form onSubmit={handleAsk} className="space-y-4">
            <label className="block text-base font-bold" htmlFor="podcast-question">
              Your question
            </label>
            <input
              id="podcast-question"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              disabled={!processed}
              className="w-full rounded-lg border border-slate-300 bg-slate-100 px-4 py-3 text-base outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30 disabled:cursor-not-allowed disabled:opacity-60 dark:border-transparent dark:bg-[#262730]"
            />
            <button
              type="submit"
              disabled={!processed || askState.loading || !question.trim()}
              className="inline-flex items-center justify-center gap-2 rounded-lg bg-[#111827] px-5 py-3 text-base font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {askState.loading && <Loader2 className="h-5 w-5 animate-spin" />}
              Ask
            </button>
          </form>

          <div className="mt-6 space-y-4">
            {askState.error && <StatusBanner type="error">Backend error while answering: {askState.error}</StatusBanner>}
            {answer && (
              <StatusBanner type="success">
                <span className="font-bold">Answer:</span> {answer}
              </StatusBanner>
            )}
          </div>
        </section>

        {models?.models && (
          <footer className="pb-6 text-sm leading-6 text-slate-500 dark:text-slate-400">
            Models: Whisper {models.models.asr}, BART {models.models.summarizer}, MiniLM {models.models.embeddings}, Gemini{" "}
            {models.models.qa}
          </footer>
        )}
      </div>
    </main>
  );
}

export default App;
