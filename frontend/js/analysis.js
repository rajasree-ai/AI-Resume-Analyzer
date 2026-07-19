// Enhanced Analysis Functions

let currentAnalysisData = null;

async function analyzeWithJobDescription() {
    const jobDesc = document.getElementById('jobDescription').value.trim();
    
    if (!jobDesc) {
        ui.showToast('Please paste a job description', 'warning');
        return;
    }

    if (!state.currentResumeId) {
        ui.showToast('Please upload a resume first', 'warning');
        return;
    }

    const btn = document.getElementById('analyzeBtn');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';

    try {
        const response = await fetch(`${API_BASE_URL}/analysis/analyze/${state.currentResumeId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                job_description: jobDesc,
                job_title: document.getElementById('jobTitle')?.value || 'Unknown Position',
                company: document.getElementById('companyName')?.value || 'Unknown Company'
            })
        });

        if (!response.ok) {
            throw new Error('Analysis failed');
        }

        const result = await response.json();
        currentAnalysisData = result.data;
        
        // Show analysis section
        document.getElementById('analysis').style.display = 'block';
        document.getElementById('analysisResults').style.display = 'block';
        
        // Render results
        renderAnalysisResults(result.data);
        
        // Show success
        ui.showToast('Analysis completed successfully!', 'success');
        
    } catch (error) {
        ui.showToast('Error: ' + error.message, 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-robot"></i> Analyze';
    }
}

function renderAnalysisResults(data) {
    // Update overall score
    updateOverallScore(data.overall_score || 0);
    
    // Update ATS and other scores
    updateScoreDetails(data);
    
    // Update skills
    updateSkills(data.matching_skills || [], data.missing_skills || []);
    
    // Update recommendations
    updateRecommendations(data.recommendations || {});
    
    // Update learning roadmap
    updateRoadmap(data.recommendations?.learning_path || []);
}

function updateOverallScore(score) {
    const circle = document.getElementById('overallScoreFill');
    const number = document.getElementById('overallScoreNumber');
    
    const circumference = 2 * Math.PI * 54;
    const offset = circumference - (score / 100) * circumference;
    
    circle.style.strokeDasharray = circumference;
    circle.style.strokeDashoffset = offset;
    
    number.textContent = Math.round(score);
}

function updateScoreDetails(data) {
    document.getElementById('atsScore').textContent = Math.round(data.keyword_match || 0) + '%';
    document.getElementById('skillsMatch').textContent = Math.round(data.skill_analysis?.match_score || 0) + '%';
    document.getElementById('experienceMatch').textContent = Math.round(data.experience_match || 0) + '%';
    document.getElementById('educationMatch').textContent = Math.round(data.education_match || 0) + '%';
}

function updateSkills(matching, missing) {
    // Update counts
    document.getElementById('matchingCount').textContent = matching.length;
    document.getElementById('missingCount').textContent = missing.length;
    
    // Render matching skills
    const matchingContainer = document.getElementById('matchingSkills');
    matchingContainer.innerHTML = matching.map(skill => 
        `<span class="skill-tag matching">${escapeHtml(skill)}</span>`
    ).join('');
    
    // Render missing skills
    const missingContainer = document.getElementById('missingSkills');
    missingContainer.innerHTML = missing.map(skill => 
        `<span class="skill-tag missing">${escapeHtml(skill)}</span>`
    ).join('');
}

function updateRecommendations(recommendations) {
    // Courses
    const coursesContainer = document.getElementById('recommendedCourses');
    if (recommendations.courses && recommendations.courses.length > 0) {
        coursesContainer.innerHTML = recommendations.courses.map(course => `
            <div class="recommendation-item">
                <div class="item-icon">
                    <i class="fas fa-book"></i>
                </div>
                <div class="item-content">
                    <h4>${escapeHtml(course.name)}</h4>
                    <p>${escapeHtml(course.platform || 'Online Course')}</p>
                    ${course.url ? `<a href="${course.url}" target="_blank" class="item-link">View Course →</a>` : ''}
                </div>
            </div>
        `).join('');
    } else {
        coursesContainer.innerHTML = '<div class="empty-state"><i class="fas fa-book empty-icon"></i><p>No course recommendations available</p></div>';
    }
    
    // Projects
    const projectsContainer = document.getElementById('recommendedProjects');
    if (recommendations.projects && recommendations.projects.length > 0) {
        projectsContainer.innerHTML = recommendations.projects.map(project => `
            <div class="recommendation-item">
                <div class="item-icon">
                    <i class="fas fa-project-diagram"></i>
                </div>
                <div class="item-content">
                    <h4>${escapeHtml(project.name)}</h4>
                    <p>${escapeHtml(project.description || '')}</p>
                </div>
            </div>
        `).join('');
    } else {
        projectsContainer.innerHTML = '<div class="empty-state"><i class="fas fa-project-diagram empty-icon"></i><p>No project recommendations available</p></div>';
    }
    
    // Certifications
    const certContainer = document.getElementById('recommendedCertifications');
    if (recommendations.certifications && recommendations.certifications.length > 0) {
        certContainer.innerHTML = recommendations.certifications.map(cert => `
            <div class="recommendation-item">
                <div class="item-icon">
                    <i class="fas fa-certificate"></i>
                </div>
                <div class="item-content">
                    <h4>${escapeHtml(cert)}</h4>
                </div>
            </div>
        `).join('');
    } else {
        certContainer.innerHTML = '<div class="empty-state"><i class="fas fa-certificate empty-icon"></i><p>No certification recommendations available</p></div>';
    }
}

function updateRoadmap(learningPath) {
    const container = document.getElementById('learningRoadmap');
    
    if (!learningPath || learningPath.length === 0) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-road empty-icon"></i><p>No learning path available</p></div>';
        return;
    }
    
    const timeline = document.createElement('div');
    timeline.className = 'timeline';
    
    learningPath.forEach((item, index) => {
        const priorityColors = {
            high: 'danger',
            medium: 'warning',
            low: 'success'
        };
        
        const timelineItem = document.createElement('div');
        timelineItem.className = 'timeline-item';
        timelineItem.innerHTML = `
            <div class="timeline-marker ${priorityColors[item.priority] || 'primary'}"></div>
            <div class="timeline-content">
                <div class="timeline-header">
                    <h4>${escapeHtml(item.skill)}</h4>
                    <span class="badge badge-${priorityColors[item.priority] || 'primary'}">${item.priority || 'medium'}</span>
                </div>
                <div class="timeline-meta">
                    <span><i class="fas fa-clock"></i> ${escapeHtml(item.estimated_time || '4-6 weeks')}</span>
                    <span><i class="fas fa-signal"></i> ${escapeHtml(item.difficulty || 'intermediate')}</span>
                </div>
            </div>
        `;
        timeline.appendChild(timelineItem);
    });
    
    container.innerHTML = '';
    container.appendChild(timeline);
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// Tab switching for recommendations
document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab-btn');
    const panels = {
        courses: document.getElementById('coursesPanel'),
        projects: document.getElementById('projectsPanel'),
        certifications: document.getElementById('certificationsPanel'),
        roadmap: document.getElementById('roadmapPanel')
    };
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Update active tab
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Show corresponding panel
            const tabId = tab.dataset.tab;
            Object.keys(panels).forEach(key => {
                panels[key].classList.toggle('active', key === tabId);
            });
        });
    });
});

// Export Functions
async function exportReport() {
    if (!currentAnalysisData) {
        ui.showToast('No analysis data to export', 'warning');
        return;
    }
    
    try {
        const analysisId = currentAnalysisData.analysis_id;
        const response = await fetch(`${API_BASE_URL}/analysis/export/${analysisId}?format=pdf`);
        
        if (!response.ok) throw new Error('Export failed');
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `resume_analysis_${analysisId}.pdf`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        
        ui.showToast('Report exported successfully!', 'success');
    } catch (error) {
        ui.showToast('Error exporting report: ' + error.message, 'error');
    }
}

async function exportJSON() {
    if (!currentAnalysisData) {
        ui.showToast('No analysis data to export', 'warning');
        return;
    }
    
    try {
        const analysisId = currentAnalysisData.analysis_id;
        const response = await fetch(`${API_BASE_URL}/analysis/export/${analysisId}?format=json`);
        
        if (!response.ok) throw new Error('Export failed');
        
        const data = await response.json();
        const json = JSON.stringify(data, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `resume_analysis_${analysisId}.json`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        
        ui.showToast('JSON exported successfully!', 'success');
    } catch (error) {
        ui.showToast('Error exporting JSON: ' + error.message, 'error');
    }
}

// Add styles for recommendation items
const recommendationStyles = document.createElement('style');
recommendationStyles.textContent = `
    .recommendation-item {
        display: flex;
        gap: var(--space-md);
        padding: var(--space-md);
        background: var(--bg-secondary);
        border-radius: var(--radius-md);
        margin-bottom: var(--space-sm);
        transition: var(--transition-base);
    }
    
    .recommendation-item:hover {
        transform: translateX(4px);
        box-shadow: var(--shadow-sm);
    }
    
    .recommendation-item .item-icon {
        width: 40px;
        height: 40px;
        border-radius: var(--radius-sm);
        background: rgba(108, 99, 255, 0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--primary);
        flex-shrink: 0;
    }
    
    .recommendation-item .item-content {
        flex: 1;
    }
    
    .recommendation-item .item-content h4 {
        font-size: var(--font-size-md);
        margin-bottom: var(--space-xs);
    }
    
    .recommendation-item .item-content p {
        font-size: var(--font-size-sm);
        color: var(--text-secondary);
        margin: 0;
    }
    
    .recommendation-item .item-link {
        display: inline-block;
        margin-top: var(--space-xs);
        font-size: var(--font-size-sm);
        color: var(--primary);
        font-weight: 500;
    }
    
    .recommendation-item .item-link:hover {
        text-decoration: underline;
    }
    
    .timeline-marker {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        position: absolute;
        left: -22px;
        top: 4px;
        border: 2px solid var(--bg-primary);
    }
    
    .timeline-marker.primary { background: var(--primary); }
    .timeline-marker.success { background: var(--success); }
    .timeline-marker.warning { background: var(--warning); }
    .timeline-marker.danger { background: var(--danger); }
    
    .timeline-header {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        margin-bottom: var(--space-xs);
    }
    
    .timeline-header h4 {
        margin: 0;
        font-size: var(--font-size-md);
    }
    
    .timeline-meta {
        display: flex;
        gap: var(--space-md);
        font-size: var(--font-size-sm);
        color: var(--text-secondary);
    }
    
    .timeline-meta i {
        margin-right: var(--space-xs);
    }
`;

document.head.appendChild(recommendationStyles);

// Make functions globally available
window.analyzeWithJobDescription = analyzeWithJobDescription;
window.exportReport = exportReport;
window.exportJSON = exportJSON;