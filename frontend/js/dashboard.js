// Dashboard functionality

function loadDashboard() {
    const dashboardSection = document.getElementById('dashboard');
    dashboardSection.style.display = 'block';
    
    // Load progress data
    loadProgressData();
    
    // Load skill development data
    loadSkillDevelopment();
}

async function loadProgressData() {
    try {
        const response = await fetch(`${API_BASE_URL}/resume/compare`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                resume_ids: [state.currentResumeId] 
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to load progress data');
        }
        
        const data = await response.json();
        renderProgressChart(data);
        
    } catch (error) {
        console.error('Error loading progress:', error);
    }
}

function renderProgressChart(data) {
    const ctx = document.getElementById('progressChartCanvas').getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.timeline || ['Current'],
            datasets: [{
                label: 'Skills Progress',
                data: data.total_skills || [0],
                borderColor: '#6C63FF',
                backgroundColor: 'rgba(108, 99, 255, 0.1)',
                borderWidth: 2,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function loadSkillDevelopment() {
    const container = document.getElementById('skillDevelopment');
    
    if (state.analysisData) {
        const skills = state.analysisData.matching_skills || [];
        const missing = state.analysisData.missing_skills || [];
        
        let html = `
            <div class="skill-stats">
                <div class="stat-card">
                    <h4>Skills Mastered</h4>
                    <span class="stat-value">${skills.length}</span>
                </div>
                <div class="stat-card">
                    <h4>Skills to Learn</h4>
                    <span class="stat-value">${missing.length}</span>
                </div>
            </div>
            <div class="skill-progress">
                <h4>Progress</h4>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${(skills.length / (skills.length + missing.length || 1)) * 100}%"></div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    } else {
        container.innerHTML = '<p>Upload and analyze a resume to see skill development</p>';
    }
}

// Add CSS for dashboard styles
const dashboardStyles = document.createElement('style');
dashboardStyles.textContent = `
    .skill-stats {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .stat-card {
        background: #F8F9FA;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    
    .stat-card h4 {
        font-size: 0.9rem;
        color: var(--gray);
        margin-bottom: 0.5rem;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
    }
    
    .skill-progress h4 {
        font-size: 0.9rem;
        color: var(--gray);
        margin-bottom: 0.5rem;
    }
    
    .timeline {
        display: grid;
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .timeline-item {
        display: grid;
        grid-template-columns: 80px 1fr;
        gap: 1rem;
        padding: 0.5rem;
        background: #F8F9FA;
        border-radius: 8px;
    }
    
    .timeline-week {
        font-weight: 600;
        color: var(--primary);
    }
    
    .timeline-tasks ul {
        list-style: none;
    }
    
    .timeline-tasks li {
        padding: 0.2rem 0;
        font-size: 0.9rem;
    }
`;

document.head.appendChild(dashboardStyles);

// Export functions
window.loadDashboard = loadDashboard;