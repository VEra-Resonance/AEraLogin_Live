/**
 * Protected Area Script
 * Loads user data and handles logout
 */

const AERA_CONFIG = {
  verifyPath: '/api/verify',
  logoutPath: '/auth/aera/logout'
};

class ProtectedArea {
  constructor() {
    this.init();
  }

  async init() {
    await this.loadUserData();
    this.setupEventListeners();
  }

  async loadUserData() {
    try {
      console.log('Loading user data...');
      const response = await fetch(AERA_CONFIG.verifyPath, {
        credentials: 'include'
      });
      
      console.log('Response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log('Verify response:', data);
        
        if (data.authenticated && data.user) {
          console.log('User authenticated, displaying data');
          this.displayUserData(data.user);
          return;
        } else {
          console.log('User not authenticated in response');
        }
      } else {
        console.log('Response not OK:', response.status);
      }
      
      // Not authenticated, redirect to home after delay
      console.log('Redirecting to home in 2 seconds...');
      setTimeout(() => {
        window.location.href = '/';
      }, 2000);
      
    } catch (err) {
      console.error('Failed to load user data:', err);
      setTimeout(() => {
        window.location.href = '/';
      }, 2000);
    }
  }

  displayUserData(user) {
    document.getElementById('wallet-address').textContent = 
      this.formatAddress(user.wallet);
    document.getElementById('user-score').textContent = user.score || '0';
    document.getElementById('user-status').textContent = 
      user.has_nft ? 'verified' : 'unverified';
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
      window.location.href = '/';
    } catch (err) {
      console.error('Logout failed:', err);
      window.location.href = '/';
    }
  }

  formatAddress(address) {
    if (!address) return '0x0000…0000';
    return `${address.substring(0, 6)}…${address.substring(address.length - 4)}`;
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
