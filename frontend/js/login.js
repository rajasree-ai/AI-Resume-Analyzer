// Auto-detect environment - this works for both local and production
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000/api'
    : window.location.origin + '/api';

function showLoginModal() {
    const modal = document.createElement('div');
    modal.className = 'login-modal-overlay';
    modal.innerHTML = `
        <div class="login-modal">
            <h2>Login</h2>
            <form id="loginForm">
                <label for="loginEmail">Email</label>
                <input type="email" id="loginEmail" required />
                <label for="loginPassword">Password</label>
                <input type="password" id="loginPassword" required />
                <button type="submit" class="btn-primary">Sign In</button>
                <button type="button" class="btn-secondary" id="loginCancel">Cancel</button>
            </form>
            <p class="login-note">Don't have an account? <a href="#" id="registerLink">Register</a></p>
        </div>
    `;

    document.body.appendChild(modal);
    document.getElementById('loginCancel').addEventListener('click', () => modal.remove());
    document.getElementById('registerLink').addEventListener('click', (e) => {
        e.preventDefault();
        modal.remove();
        showRegisterModal();
    });

    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        const success = await loginUser(email, password);
        if (success) {
            modal.remove();
        }
    });
}

function showRegisterModal() {
    const modal = document.createElement('div');
    modal.className = 'login-modal-overlay';
    modal.innerHTML = `
        <div class="login-modal">
            <h2>Register</h2>
            <form id="registerForm">
                <label for="registerUsername">Username</label>
                <input type="text" id="registerUsername" required />
                <label for="registerEmail">Email</label>
                <input type="email" id="registerEmail" required />
                <label for="registerPassword">Password</label>
                <input type="password" id="registerPassword" required />
                <button type="submit" class="btn-primary">Create Account</button>
                <button type="button" class="btn-secondary" id="registerCancel">Cancel</button>
            </form>
        </div>
    `;

    document.body.appendChild(modal);
    document.getElementById('registerCancel').addEventListener('click', () => modal.remove());

    document.getElementById('registerForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('registerUsername').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        await registerUser(username, email, password);
        modal.remove();
    });
}

async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Login failed');
        localStorage.setItem('accessToken', result.access_token);
        localStorage.setItem('user', JSON.stringify(result.user));
        showSuccess('Logged in successfully');
        updateLoginState();
        return true;
    } catch (error) {
        showError(error.message);
        return false;
    }
}

async function registerUser(username, email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Registration failed');
        localStorage.setItem('accessToken', result.access_token);
        localStorage.setItem('user', JSON.stringify(result.user));
        showSuccess('Account created successfully');
        updateLoginState();
    } catch (error) {
        showError(error.message);
    }
}

function updateLoginState() {
    const user = JSON.parse(localStorage.getItem('user') || 'null');
    const loginButton = document.querySelector('.btn-login');
    if (user) {
        loginButton.textContent = `Hi, ${user.username}`;
        loginButton.disabled = true;
    } else {
        loginButton.textContent = 'Login';
        loginButton.disabled = false;
    }
}

window.showLoginModal = showLoginModal;
window.showRegisterModal = showRegisterModal;
window.loginUser = loginUser;
window.registerUser = registerUser;
