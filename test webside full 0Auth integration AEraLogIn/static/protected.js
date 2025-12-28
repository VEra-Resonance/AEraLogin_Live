/**
 * Protected Area Script
 * Zero-Trust Implementation: Content loaded ONLY after server verification
 */

// Auto-detect URL prefix from current path
const URL_PREFIX = window.location.pathname.split('/').slice(0, 2).join('/') || '';

const AERA_CONFIG = {
  verifyPath: `${URL_PREFIX}/api/verify`,
  logoutPath: `${URL_PREFIX}/auth/aera/logout`,
  homePath: `${URL_PREFIX}/`
};

console.log('[PROTECTED] URL_PREFIX:', URL_PREFIX);
console.log('[PROTECTED] Config:', AERA_CONFIG);

class ProtectedArea {
  constructor() {
    this.init();
  }

  async init() {
    await this.loadUserData();
  }

  async loadUserData() {
    try {
      console.log('[SECURITY] Verifying token with server...');
      const response = await fetch(AERA_CONFIG.verifyPath, {
        credentials: 'include'
      });
      
      console.log('[SECURITY] Response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log('[SECURITY] Verify response:', data);
        
        if (data.authenticated && data.user) {
          console.log('[SECURITY] ✅ Token verified - Loading protected content');
          this.showProtectedContent(data.user);
          return;
        } else {
          console.log('[SECURITY] ❌ Not authenticated');
        }
      } else {
        console.log('[SECURITY] ❌ Verification failed:', response.status);
      }
      
      // Not authenticated - immediate redirect (no content shown)
      console.log('[SECURITY] Redirecting to login...');
      this.redirectToLogin();
      
    } catch (err) {
      console.error('[SECURITY] ❌ Verification error:', err);
      this.redirectToLogin();
    }
  }

  showProtectedContent(user) {
    // Hide verification overlay
    const overlay = document.getElementById('verification-overlay');
    if (overlay) {
      overlay.style.display = 'none';
    }

    // Show protected content (add class for flex centering)
    const content = document.getElementById('protected-content');
    if (content) {
      content.classList.add('visible');
    }

    // Dynamically inject user data (AFTER verification)
    const container = document.getElementById('user-data-container');
    if (container) {
      container.innerHTML = `
        <div class="data">
          <p><strong>Wallet:</strong> <code>${this.formatAddress(user.wallet)}</code></p>
          <p><strong>Score:</strong> <span class="score-badge">${user.score || '0'}</span></p>
          <p><strong>Status:</strong> <span class="status-badge status-${user.has_nft ? 'verified' : 'unverified'}">${user.has_nft ? '✅ Verified' : '❌ Unverified'}</span></p>
          <p><strong>Session Expires:</strong> ${this.formatExpiry(user.expires_at)}</p>
        </div>
      `;
    }

    // Setup event listeners after content is shown
    this.setupEventListeners();
  }

  redirectToLogin() {
    // Show error message briefly before redirect
    const overlay = document.getElementById('verification-overlay');
    if (overlay) {
      overlay.innerHTML = `
        <div class="verification-spinner">
          <div style="font-size: 3rem; margin-bottom: 1rem;">🔒</div>
          <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">Access Denied</p>
          <p style="opacity: 0.7;">Redirecting to login...</p>
        </div>
      `;
    }
    
    setTimeout(() => {
      window.location.href = AERA_CONFIG.homePath;
    }, 1500);
  }

  setupEventListeners() {
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', () => this.logout());
    }
  }

  async logout() {
    try {
      await fetch(AERA_CONFIG.logoutPath, {
        method: 'POST',
        credentials: 'include'
      });
      window.location.href = AERA_CONFIG.homePath;
    } catch (err) {
      console.error('Logout failed:', err);
      window.location.href = AERA_CONFIG.homePath;
    }
  }

  formatAddress(address) {
    if (!address) return '0x0000…0000';
    return `${address.substring(0, 6)}…${address.substring(address.length - 4)}`;
  }

  formatExpiry(expiresAt) {
    if (!expiresAt) return 'Unknown';
    try {
      const date = new Date(expiresAt);
      const now = new Date();
      const diffMs = date - now;
      const diffMins = Math.floor(diffMs / 60000);
      
      if (diffMins < 60) {
        return `in ${diffMins} minutes`;
      } else {
        const diffHours = Math.floor(diffMins / 60);
        return `in ${diffHours} hour${diffHours > 1 ? 's' : ''}`;
      }
    } catch {
      return 'Unknown';
    }
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    new ProtectedArea();
  });
} else {
  new ProtectedArea();
}
