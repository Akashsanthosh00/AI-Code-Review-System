let lastReport = "";

const inputCode = document.getElementById("inputCode");
const outputBox = document.getElementById("outputResult");
const highlightedCode = document.getElementById("highlightedCode");
const fileInput = document.getElementById("fileInput");
const downloadBtn = document.getElementById("downloadBtn");

fileInput.addEventListener("change", handleFileUpload);

async function reviewCode() {
    const code = inputCode.value.trim();

    if (!code) {
        outputBox.textContent = "Please paste some code first or upload a file.";
        highlightedCode.innerHTML = `<div class="empty-state">No code available to highlight.</div>`;
        downloadBtn.disabled = true;
        return;
    }

    outputBox.textContent = "Analyzing code...";
    highlightedCode.innerHTML = `<div class="empty-state">Preparing highlighted view...</div>`;
    downloadBtn.disabled = true;

    try {
        const response = await fetch("/review", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code: code })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        const report = data.report || "No report was returned.";

        lastReport = report;
        outputBox.textContent = report;
        downloadBtn.disabled = false;

        const issueRanges = extractIssueRanges(report);
        renderHighlightedCode(code, issueRanges);

    } catch (error) {
        outputBox.textContent = `Error: ${error.message}`;
        highlightedCode.innerHTML = `<div class="empty-state">Could not generate highlighted code view.</div>`;
        downloadBtn.disabled = true;
    }
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();

    reader.onload = function (e) {
        inputCode.value = e.target.result;
        outputBox.textContent = `File loaded successfully: ${file.name}`;
        highlightedCode.innerHTML = `<div class="empty-state">Click "Review Code" to analyze the uploaded file.</div>`;
    };

    reader.onerror = function () {
        outputBox.textContent = "Failed to read the selected file.";
    };

    reader.readAsText(file);
}

function clearAll() {
    inputCode.value = "";
    outputBox.textContent = "The review report will appear here...";
    highlightedCode.innerHTML = `<div class="empty-state">Reviewed code with highlighted issue lines will appear here...</div>`;
    fileInput.value = "";
    lastReport = "";
    downloadBtn.disabled = true;
}

function downloadReport() {
    if (!lastReport) return;

    const blob = new Blob([lastReport], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "ai_code_review_report.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    URL.revokeObjectURL(url);
}

function extractIssueRanges(reportText) {
    const ranges = [];
    const regex = /Lines\s*:\s*(\d+)(?:\s*-\s*(\d+))?/gi;
    let match;

    while ((match = regex.exec(reportText)) !== null) {
        const start = parseInt(match[1], 10);
        const end = match[2] ? parseInt(match[2], 10) : start;

        if (!isNaN(start) && !isNaN(end)) {
            ranges.push({ start, end });
        }
    }

    return ranges;
}

function isLineHighlighted(lineNumber, ranges) {
    return ranges.some(range => lineNumber >= range.start && lineNumber <= range.end);
}

function renderHighlightedCode(code, ranges) {
    const lines = code.split("\n");

    if (!code.trim()) {
        highlightedCode.innerHTML = `<div class="empty-state">No code available to display.</div>`;
        return;
    }

    let html = "";

    lines.forEach((line, index) => {
        const lineNumber = index + 1;
        const highlighted = isLineHighlighted(lineNumber, ranges) ? "highlight" : "";
        html += `
            <div class="code-line ${highlighted}">
                <div class="line-number">${lineNumber}</div>
                <div class="line-content">${escapeHtml(line) || "&nbsp;"}</div>
            </div>
        `;
    });

    highlightedCode.innerHTML = html;
}

function escapeHtml(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}