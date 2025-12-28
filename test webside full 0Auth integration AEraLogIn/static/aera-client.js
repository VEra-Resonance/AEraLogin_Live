/**
 * AEra Client Integration
 * Handles authentication flow and protected content display
 */

// Auto-detect URL prefix from current path
const URL_PREFIX = window.location.pathname.split('/').slice(0, 2).join('/') || '';

const AERA_CONFIG = {
  baseUrl: window.location.origin,
  loginPath: `${URL_PREFIX}/auth/aera/login`,
  logoutPath: `${URL_PREFIX}/auth/aera/logout`,
  verifyPath: `${URL_PREFIX}/api/verify`
};

console.log('[AERA] Initialized with URL_PREFIX:', URL_PREFIX);
console.log('[AERA] Config:', AERA_CONFIG);

class AEraClient {
  constructor() {
    this.user = null;
    this.init();
  }

  async init() {
    // Check if user is already authenticated
    await this.checkAuth();
    this.setupEventListeners();
  }

  async checkAuth() {
    try {
      const response = await fetch(AERA_CONFIG.verifyPath, {
        credentials: 'include'
      });
      
      if (response.ok) {
        const data = await response.json();
        if (data.authenticated) {
          this.user = data.user;
          this.showAuthenticated();
          return true;
        }
      }
    } catch (err) {
      console.error('Auth check failed:', err);
    }
    
    this.showLanding();
    return false;
  }

  setupEventListeners() {
    const loginBtn = document.getElementById('login-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const showProtectedBtn = document.getElementById('show-protected-btn');
    const hideProtectedBtn = document.getElementById('hide-protected-btn');

    if (loginBtn) {
      loginBtn.addEventListener('click', () => this.login());
    }

    if (logoutBtn) {
      logoutBtn.addEventListener('click', () => this.logout());
    }

    if (showProtectedBtn) {
      showProtectedBtn.addEventListener('click', () => this.showProtected());
    }

    if (hideProtectedBtn) {
      hideProtectedBtn.addEventListener('click', () => this.hideProtected());
    }
  }

  login() {
    // Redirect to AEra OAuth login
    window.location.href = AERA_CONFIG.loginPath;
  }

  async logout() {
    try {
      await fetch(AERA_CONFIG.logoutPath, {
        method: 'POST',
        credentials: 'include'
      });
      this.user = null;
      this.showLanding();
    } catch (err) {
      console.error('Logout failed:', err);
    }
  }

  showLanding() {
    document.getElementById('landing').style.display = 'block';
    document.getElementById('authenticated').style.display = 'none';
    document.getElementById('protected').style.display = 'none';
  }

  showAuthenticated() {
    document.getElementById('landing').style.display = 'none';
    document.getElementById('authenticated').style.display = 'block';
    document.getElementById('protected').style.display = 'none';
  }

  showProtected() {
    if (!this.user) return;

    // SECURITY: Dynamically inject user data ONLY after verification
    const container = document.getElementById('protected-data-container');
    if (container) {
      container.innerHTML = `
        <div class="data">
          <p><strong>Wallet:</strong> <code>${this.formatAddress(this.user.wallet)}</code></p>
          <p><strong>Score:</strong> <span class="score-badge">${this.user.score || '0'}</span></p>
          <p><strong>Status:</strong> <span class="status-badge status-${this.user.has_nft ? 'verified' : 'unverified'}">${this.user.has_nft ? '✅ Verified' : '❌ Unverified'}</span></p>
        </div>
      `;
    }

    document.getElementById('landing').style.display = 'none';
    document.getElementById('authenticated').style.display = 'none';
    document.getElementById('protected').style.display = 'block';
  }

  hideProtected() {
    // SECURITY: Clear sensitive data when hiding
    const container = document.getElementById('protected-data-container');
    if (container) {
      container.innerHTML = '';
    }
    this.showAuthenticated();
  }

  formatAddress(address) {
    if (!address) return '0x0000…0000';
    return `${address.substring(0, 6)}…${address.substring(address.length - 4)}`;
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new AEraClient();
  });
} else {
  new AEraClient();
}
