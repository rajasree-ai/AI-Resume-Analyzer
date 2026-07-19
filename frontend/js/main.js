// Main JavaScript for AI Resume Skill Gap Analyzer

// API Configuration
const API_BASE_URL = '/api';

// State Management
let state = {
    currentResumeId: null,
    analysisData: null,
    charts: {}
};

// Utility Functions
function showError(message) {
    alert(message);
}

function showSuccess(message) {
    alert(message);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const section = this.getAttribute('href').substring(1);

        // Update active nav link
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        this.classList.add('active');

        // Show/hide sections
        document.querySelectorAll('section').forEach(s => s.style.display = 'none');
        const targetSection = document.getElementById(section);
        if (targetSection) targetSection.style.display = 'block';
    });
});

// Choose file button
const chooseFileBtn = document.getElementById('chooseFileBtn');
if (chooseFileBtn) {
    chooseFileBtn.addEventListener('click', () => document.getElementById('fileInput')?.click());
}

// Keyboard support for upload dropzone
const uploadArea = document.getElementById('uploadArea');
if (uploadArea) {
    uploadArea.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            document.getElementById('fileInput')?.click();
        }
    });
}

function setUploadStatus(html, type) {
    const el = document.getElementById('uploadStatus');
    if (!el) return;
    const cls = type ? `alert-inline ${type}` : 'alert-inline';
    el.innerHTML = `<div class="${cls}">${html}</div>`;
}

function setLoading(isLoading) {
    const progressDiv = document.getElementById('uploadProgress');
    const fill = document.querySelector('.progress-fill');
    const text = document.querySelector('.progress-text');

    if (!progressDiv || !fill || !text) return;

    if (isLoading) {
        progressDiv.style.display = 'block';
        fill.style.width = '35%';
        text.textContent = 'Uploading...';
    } else {
        progressDiv.style.display = 'none';
        fill.style.width = '0%';
    }
}


// Login button
window.updateLoginState = function() {
    const user = JSON.parse(localStorage.getItem('user') || 'null');
    const loginButton = document.querySelector('.btn-login');
    if (loginButton) {
        if (user) {
            loginButton.textContent = `Hi, ${user.username}`;
            loginButton.disabled = true;
        } else {
            loginButton.textContent = 'Login';
            loginButton.disabled = false;
        }
    }
};

window.addEventListener('load', () => {
    updateLoginState();
    const loginButton = document.querySelector('.btn-login');
    if (loginButton && typeof showLoginModal === 'function') {
        loginButton.addEventListener('click', showLoginModal);
    }
});

// File upload handling
document.getElementById('fileInput').addEventListener('change', function(e) {
    const file = this.files[0];
    if (file) {
        handleFileUpload(file);
    }
});

// Drag and drop
const uploadArea = document.getElementById('uploadArea');

uploadArea.addEventListener('dragover', function(e) {
    e.preventDefault();
    this.style.borderColor = 'var(--primary)';
    this.style.background = 'rgba(108, 99, 255, 0.05)';
});

uploadArea.addEventListener('dragleave', function(e) {
    e.preventDefault();
    this.style.borderColor = 'var(--light-gray)';
    this.style.background = 'transparent';
});

uploadArea.addEventListener('drop', function(e) {
    e.preventDefault();
    this.style.borderColor = 'var(--light-gray)';
    this.style.background = 'transparent';
    
    const file = e.dataTransfer.files[0];
    if (file) {
        document.getElementById('fileInput').files = e.dataTransfer.files;
        handleFileUpload(file);
    }
});

async function handleFileUpload(file) {
    const formData = new FormData();
    formData.append('resume', file);

    // Show progress
    setLoading(true);
    setUploadStatus('', null);

    try {
        const response = await fetch(`${API_BASE_URL}/resume/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const err = await response.json().catch(() => null);
            throw new Error(err?.error || 'Upload failed');
        }

        const data = await response.json();
        state.currentResumeId = data.resume_id;

        // Update progress
        const fill = document.querySelector('.progress-fill');
        const progressText = document.querySelector('.progress-text');
        if (fill) fill.style.width = '100%';
        if (progressText) progressText.textContent = 'Upload complete!';

        setUploadStatus(`✅ Resume uploaded successfully.`, 'success');

        const uploadStatus = document.getElementById('uploadStatus');
        if (uploadStatus) {
            uploadStatus.innerHTML += `
                <div style="margin-top: 0.75rem; display:flex; justify-content:center;">
                    <button class="btn-upload" type="button" onclick="analyzeResume(${data.resume_id})">Analyze Now</button>
                </div>
            `;
        }

        setTimeout(() => setLoading(false), 900);

    } catch (error) {
        setLoading(false);
        setUploadStatus(`❌ Error uploading resume: ${error.message}`, 'error');
    }
}


async function analyzeResume(resumeId) {
    const jobDescription = prompt('Paste the job description to analyze against:');
    if (!jobDescription) return;

    try {
        setUploadStatus('🔎 Analyzing... please wait', null);

        const response = await fetch(`${API_BASE_URL}/resume/analyze/${resumeId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ job_description: jobDescription })
        });

        if (!response.ok) {
            const err = await response.json().catch(() => null);
            throw new Error(err?.error || 'Analysis failed');
        }

        const data = await response.json();
        state.analysisData = data;

        // Show analysis section
        document.getElementById('analysis-section').style.display = 'block';

        // Update top summary banner
        const summaryCompatibility = document.getElementById('summaryCompatibility');
        const summaryAts = document.getElementById('summaryAts');
        const summarySkillMatch = document.getElementById('summarySkillMatch');

        if (summaryCompatibility) summaryCompatibility.textContent = `${Math.round(data.compatibility_score || 0)}%`;
        if (summaryAts) summaryAts.textContent = `${Math.round(data.ats_score || 0)}`;
        if (summarySkillMatch) summarySkillMatch.textContent = `${Math.round(data.skill_match_rate || 0)}%`;

        // Render analysis results
        renderAnalysis(data);

        // Scroll to analysis
        document.getElementById('analysis-section').scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        setUploadStatus(`❌ Error analyzing resume: ${error.message}`, 'error');
    }
}


// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize any charts or components
});

// Export functions for use in other scripts
window.analyzeResume = analyzeResume;