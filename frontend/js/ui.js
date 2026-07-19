// UI Utilities and Components

class UI {
    constructor() {
        this.toastContainer = document.getElementById('toastContainer');
        this.modal = document.getElementById('loginModal');
        this.theme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        this.setupTheme();
        this.setupModal();
        this.setupMobileMenu();
        this.setupNavbarScroll();
        this.setupSmoothScroll();
        this.setupCounterAnimation();
        this.setupParticles();
    }

    // Theme Management
    setupTheme() {
        const toggle = document.getElementById('themeToggle');
        const icon = toggle.querySelector('i');
        
        if (this.theme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
            icon.className = 'fas fa-sun';
        }

        toggle.addEventListener('click', () => {
            this.theme = this.theme === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', this.theme);
            localStorage.setItem('theme', this.theme);
            icon.className = this.theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        });
    }

    // Modal Management
    setupModal() {
        const loginBtn = document.getElementById('loginBtn');
        const closeBtn = document.getElementById('closeModal');
        const modal = this.modal;

        loginBtn.addEventListener('click', () => this.openModal());
        closeBtn.addEventListener('click', () => this.closeModal());
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) this.closeModal();
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') this.closeModal();
        });
    }

    openModal() {
        this.modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    closeModal() {
        this.modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    // Mobile Menu
    setupMobileMenu() {
        const btn = document.getElementById('mobileMenuBtn');
        const menu = document.getElementById('navMenu');
        const icon = btn.querySelector('i');

        btn.addEventListener('click', () => {
            menu.classList.toggle('active');
            icon.className = menu.classList.contains('active') 
                ? 'fas fa-times' 
                : 'fas fa-bars';
        });

        // Close menu on link click
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                menu.classList.remove('active');
                icon.className = 'fas fa-bars';
            });
        });
    }

    // Navbar Scroll Effect
    setupNavbarScroll() {
        const navbar = document.getElementById('navbar');
        let lastScroll = 0;

        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            
            if (currentScroll > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }

            lastScroll = currentScroll;
        });
    }

    // Smooth Scroll
    setupSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href === '#') return;
                
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // Counter Animation
    setupCounterAnimation() {
        const counters = document.querySelectorAll('[data-count]');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = parseInt(entry.target.getAttribute('data-count'));
                    this.animateCounter(entry.target, target);
                    observer.unobserve(entry.target);
                }
            });
        });

        counters.forEach(counter => observer.observe(counter));
    }

    animateCounter(element, target) {
        let current = 0;
        const increment = Math.ceil(target / 60);
        const duration = 2000;
        const stepTime = duration / 60;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = current;
        }, stepTime);
    }

    // Particles Background
    setupParticles() {
        const container = document.getElementById('heroParticles');
        if (!container) return;

        // Simple particle effect
        const particles = [];
        const count = 50;

        for (let i = 0; i < count; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.cssText = `
                position: absolute;
                width: ${Math.random() * 4 + 2}px;
                height: ${Math.random() * 4 + 2}px;
                background: rgba(108, 99, 255, ${Math.random() * 0.3 + 0.1});
                border-radius: 50%;
                top: ${Math.random() * 100}%;
                left: ${Math.random() * 100}%;
                animation: float-particle ${Math.random() * 20 + 10}s linear infinite;
                animation-delay: ${Math.random() * -10}s;
            `;
            container.appendChild(particle);
            particles.push(particle);
        }

        // Add keyframes dynamically
        const style = document.createElement('style');
        style.textContent = `
            @keyframes float-particle {
                0% { transform: translate(0, 0) scale(1); opacity: ${Math.random() * 0.5 + 0.3}; }
                25% { transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * -50}px) scale(${Math.random() * 0.5 + 0.5}); }
                50% { transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * -100}px) scale(${Math.random() * 0.5 + 0.5}); }
                75% { transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * -50}px) scale(${Math.random() * 0.5 + 0.5}); }
                100% { transform: translate(0, 0) scale(1); opacity: ${Math.random() * 0.5 + 0.3}; }
            }
        `;
        document.head.appendChild(style);
    }

    // Toast Notifications
    showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };

        toast.innerHTML = `
            <div class="toast-icon">
                <i class="${icons[type] || icons.info}"></i>
            </div>
            <div class="toast-content">
                <div class="toast-title">${type.charAt(0).toUpperCase() + type.slice(1)}</div>
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close">
                <i class="fas fa-times"></i>
            </button>
        `;

        this.toastContainer.appendChild(toast);

        // Auto dismiss
        const timer = setTimeout(() => {
            toast.remove();
        }, duration);

        // Manual dismiss
        toast.querySelector('.toast-close').addEventListener('click', () => {
            clearTimeout(timer);
            toast.remove();
        });

        // Hover to pause
        toast.addEventListener('mouseenter', () => clearTimeout(timer));
        toast.addEventListener('mouseleave', () => {
            setTimeout(() => toast.remove(), duration);
        });
    }

    // Loading State
    showLoading(container) {
        const loader = document.createElement('div');
        loader.className = 'loading-overlay';
        loader.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner"></div>
                <p>Loading...</p>
            </div>
        `;
        container.style.position = 'relative';
        container.appendChild(loader);
    }

    hideLoading(container) {
        const loader = container.querySelector('.loading-overlay');
        if (loader) loader.remove();
    }

    // Scroll to Element
    scrollToElement(element, offset = 80) {
        const rect = element.getBoundingClientRect();
        const targetScroll = window.pageYOffset + rect.top - offset;
        window.scrollTo({
            top: targetScroll,
            behavior: 'smooth'
        });
    }
}

// Initialize UI
const ui = new UI();

// Make UI globally accessible
window.ui = ui;

// Helper Functions
function scrollToSection(id) {
    const element = document.getElementById(id);
    if (element) {
        ui.scrollToElement(element);
    }
}

function playDemo() {
    ui.showToast('Demo video coming soon!', 'info', 3000);
}

function showNotification(message, type = 'info') {
    ui.showToast(message, type);
}

// Export for use in other scripts
export default UI;