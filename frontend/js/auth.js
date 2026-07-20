// =============================================
// AUTHENTICATION FUNCTIONS
// =============================================

// Auto-detect environment - this works for both local and production
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000/api'
    : window.location.origin + '/api';
let authToken = localStorage.getItem('authToken');
let currentUser = null;

// =============================================
// DOM ELEMENTS
// =============================================
const authModal = document.getElementById('authModal');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const resetForm = document.getElementById('resetForm');

// =============================================
// MODAL CONTROLS
// =============================================
function openAuthModal() {
    if (authModal) {
        authModal.classList.add('active');
        showLogin();
    }
}

function closeAuthModal() {
    if (authModal) {
        authModal.classList.remove('active');
    }
}

function showLogin() {
    if (loginForm) loginForm.classList.add('active');
    if (registerForm) registerForm.classList.remove('active');
    if (resetForm) resetForm.classList.remove('active');
}

function showRegister() {
    if (registerForm) registerForm.classList.add('active');
    if (loginForm) loginForm.classList.remove('active');
    if (resetForm) resetForm.classList.remove('active');
}

function showResetPassword() {
    if (resetForm) resetForm.classList.add('active');
    if (loginForm) loginForm.classList.remove('active');
    if (registerForm) registerForm.classList.remove('active');
}

// Close modal on outside click
if (authModal) {
    authModal.addEventListener('click', (e) => {
        if (e.target === authModal) {
            closeAuthModal();
        }
    });
}

// Close on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && authModal && authModal.classList.contains('active')) {
        closeAuthModal();
    }
});

// Close button
const closeBtn = document.getElementById('closeAuthModal');
if (closeBtn) {
    closeBtn.addEventListener('click', closeAuthModal);
}

// =============================================
// REGISTER USER
// =============================================
async function registerUser() {
    const username = document.getElementById('registerUsername')?.value?.trim() || '';
    const email = document.getElementById('registerEmail')?.value?.trim() || '';
    const password = document.getElementById('registerPassword')?.value || '';
    const fullName = document.getElementById('registerFullName')?.value?.trim() || '';

    if (!username || !email || !password) {
        showToast('Please fill in all required fields', 'warning');
        return;
    }

    if (password.length < 6) {
        showToast('Password must be at least 6 characters', 'warning');
        return;
    }

    const btn = document.querySelector('#registerForm .btn-full');
    if (!btn) return;
    
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating...';

    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                email,
                password,
                full_name: fullName
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Registration failed');
        }

        if (data.token) {
            localStorage.setItem('authToken', data.token);
            authToken = data.token;
            currentUser = data.user;
            updateUIForLoggedInUser();
            closeAuthModal();
            showToast('Registration successful! Welcome ' + data.user.username, 'success');
        }

    } catch (error) {
        showToast('Registration failed: ' + error.message, 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
}

// =============================================
// LOGIN USER
// =============================================
async function loginUser() {
    const email = document.getElementById('loginEmail')?.value?.trim() || '';
    const password = document.getElementById('loginPassword')?.value || '';
    const remember = document.getElementById('rememberMe')?.checked || false;

    if (!email || !password) {
        showToast('Please enter email and password', 'warning');
        return;
    }

    const btn = document.querySelector('#loginForm .btn-full');
    if (!btn) return;
    
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Signing in...';

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email,
                password,
                remember
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Login failed');
        }

        if (data.token) {
            localStorage.setItem('authToken', data.token);
            authToken = data.token;
            currentUser = data.user;
            updateUIForLoggedInUser();
            closeAuthModal();
            showToast('Welcome back, ' + data.user.username + '!', 'success');
        }

    } catch (error) {
        showToast('Login failed: ' + error.message, 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
}

// =============================================
// RESET PASSWORD
// =============================================
async function resetPassword() {
    const email = document.getElementById('resetEmail')?.value?.trim() || '';

    if (!email) {
        showToast('Please enter your email', 'warning');
        return;
    }

    const btn = document.querySelector('#resetForm .btn-full');
    if (!btn) return;
    
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

    try {
        const response = await fetch(`${API_BASE_URL}/auth/reset-password-request`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }

        showToast('Check your email for reset link', 'success');
        showLogin();

    } catch (error) {
        showToast('Error: ' + error.message, 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
}

// =============================================
// LOGOUT
// =============================================
function logoutUser() {
    localStorage.removeItem('authToken');
    authToken = null;
    currentUser = null;
    updateUIForLoggedOutUser();
    showToast('Logged out successfully', 'info');
}

// =============================================
// CHECK AUTH STATUS
// =============================================
async function checkAuth() {
    if (!authToken) {
        updateUIForLoggedOutUser();
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/auth/me`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (!response.ok) {
            throw new Error('Session expired');
        }

        const data = await response.json();
        currentUser = data.user;
        updateUIForLoggedInUser();

    } catch (error) {
        localStorage.removeItem('authToken');
        authToken = null;
        currentUser = null;
        updateUIForLoggedOutUser();
    }
}

// =============================================
// UPDATE UI FOR LOGGED IN USER
// =============================================
function updateUIForLoggedInUser() {
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn && currentUser) {
        loginBtn.innerHTML = `<i class="fas fa-user-check"></i> ${currentUser.username}`;
        loginBtn.className = 'btn-login';
        loginBtn.onclick = () => {
            if (confirm(`Logout ${currentUser.username}?`)) {
                logoutUser();
            }
        };
    }
}

// =============================================
// UPDATE UI FOR LOGGED OUT USER
// =============================================
function updateUIForLoggedOutUser() {
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) {
        loginBtn.innerHTML = '<i class="fas fa-user"></i> Sign In';
        loginBtn.className = 'btn-login';
        loginBtn.onclick = () => openAuthModal();
    }
}

// =============================================
// MAKE FUNCTIONS AVAILABLE GLOBALLY
// =============================================
window.registerUser = registerUser;
window.loginUser = loginUser;
window.resetPassword = resetPassword;
window.logoutUser = logoutUser;
window.openAuthModal = openAuthModal;
window.closeAuthModal = closeAuthModal;
window.showLogin = showLogin;
window.showRegister = showRegister;
window.showResetPassword = showResetPassword;
window.checkAuth = checkAuth;

// =============================================
// INITIALIZE ON PAGE LOAD
// =============================================
document.addEventListener('DOMContentLoaded', () => {
    // Check authentication status
    checkAuth();

    // Set up login button if it exists
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn && !currentUser) {
        loginBtn.onclick = () => openAuthModal();
    }
});

console.log('🔐 Auth.js loaded successfully!');