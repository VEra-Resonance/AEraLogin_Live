"""
AEra Gate Flask Server
Minimal Flask server with AEra OAuth integration
"""

from flask import Flask, request, session, redirect, jsonify, send_from_directory
from dotenv import load_dotenv
import os
import secrets
import requests
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))
# Production Security Settings
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=3600,
    SESSION_COOKIE_NAME='__Host-session'
)

# CSRF Protection
csrf = CSRFProtect(app)

# Rate Limiting
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Security Headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

def safe_log_token(token):
    if token and len(token) > 20:
        return f"{token[:10]}...{token[-10:]}"
    return "***"

# AEra Configuration
AERA_CONFIG = {
    'base_url': os.environ.get('AERA_BASE_URL', 'https://aeralogin.com'),
    'client_id': os.environ.get('AERA_CLIENT_ID', ''),
    'client_secret': os.environ.get('AERA_CLIENT_SECRET', ''),
    'session_name': 'aera_token',
    'require_nft': False,  # Temporarily disabled for testing
    'min_score': 0
}


def verify_token(token):
    """
    Verify AEra access token with /api/v1/verify endpoint
    NOW FIXED by AEra Team (22.12.2025) - audience validation disabled
    """
    try:
        print(f"[TOKEN_VERIFY] Verifying token with /api/v1/verify... Token: {safe_log_token(token)}")
        response = requests.post(
            f"{AERA_CONFIG['base_url']}/api/v1/verify",
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
            timeout=10
        )
        print(f"[TOKEN_VERIFY] Response status: {response.status_code}")
        # Nur Status loggen, keine sensiblen Daten
        if response.status_code == 200:
            data = response.json()
            
            # Check both 'valid' AND 'authenticated' (as per AEra's fix)
            if data.get('valid') and data.get('authenticated'):
                print(f"[TOKEN_VERIFY] ✅ SUCCESS! Token is valid and authenticated")
                print(f"[TOKEN_VERIFY] User: {data.get('wallet')}")
                print(f"[TOKEN_VERIFY] Score: {data.get('score')}")
                print(f"[TOKEN_VERIFY] Has NFT: {data.get('has_nft')}")
                print(f"[TOKEN_VERIFY] Expires: {data.get('expires_at')}")
                
                return {
                    'wallet': data.get('wallet'),
                    'score': data.get('score', 0),
                    'has_nft': data.get('has_nft', False),
                    'chain_id': data.get('chain_id'),
                    'issued_at': data.get('issued_at'),
                    'expires_at': data.get('expires_at'),
                    'client_id': data.get('client_id'),
                    'jti': data.get('jti')
                }
            else:
                error_msg = data.get('error', 'Unknown error')
                print(f"[TOKEN_VERIFY] ❌ FAILED: valid={data.get('valid')}, authenticated={data.get('authenticated')}")
                print(f"[TOKEN_VERIFY] Error: {error_msg}")
                return None
        else:
            print(f"[TOKEN_VERIFY] ❌ HTTP Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"[TOKEN_VERIFY] ❌ Exception: {e}")
        return None


def exchange_code(code, redirect_uri):
    """Exchange authorization code for access token"""
    try:
        # Exchange code for token
        print(f"[EXCHANGE] ===== TOKEN EXCHANGE =====")
        print(f"[EXCHANGE] Exchanging code for token...")
        response = requests.post(
            f"{AERA_CONFIG['base_url']}/oauth/token",
            json={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': redirect_uri,
                'client_id': AERA_CONFIG['client_id'],
                'client_secret': AERA_CONFIG['client_secret']
            },
            timeout=10
        )
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"[EXCHANGE] ===== COMPLETE RESPONSE =====")
            print(f"[EXCHANGE] Status Code: {response.status_code}")
            print(f"[EXCHANGE] Response Keys: {list(token_data.keys())}")
            for key, value in token_data.items():
                if isinstance(value, str) and len(value) > 100:
                    print(f"[EXCHANGE] {key}: {value[:50]}...{value[-20:]}")
                else:
                    print(f"[EXCHANGE] {key}: {value}")
            print(f"[EXCHANGE] ===== END RESPONSE =====")
            return token_data
        else:
            print(f"[EXCHANGE] Failed with status: {response.status_code}")
            print(f"[EXCHANGE] Response: {response.text}")
                
    except Exception as e:
        print(f"[EXCHANGE] Exception: {e}")
    
    return None


@app.route('/')
def index():
    """Serve main page"""
    return send_from_directory('.', 'index.html')


@app.route('/protected')
def protected():
    """Serve protected area page"""
    return send_from_directory('.', 'protected.html')


@app.route('/style.css')
def styles():
    """Serve CSS"""
    return send_from_directory('.', 'style.css')


@app.route('/auth/aera/login')
@limiter.limit("5 per minute")
def aera_login():
    """Redirect to AEra OAuth login"""
    state = secrets.token_urlsafe(32)
    session['aera_state'] = state
    session['aera_return_to'] = request.args.get('next', '/')
    
    # Build redirect URI with proper scheme (handle ngrok HTTPS)
    scheme = request.headers.get('X-Forwarded-Proto', request.scheme)
    host = request.headers.get('X-Forwarded-Host', request.host)
    redirect_uri = f"{scheme}://{host}/auth/aera/callback"
    
    auth_url = (
        f"{AERA_CONFIG['base_url']}/oauth/authorize"
        f"?client_id={AERA_CONFIG['client_id']}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&state={state}"
    )
    
    return redirect(auth_url)


@app.route('/auth/aera/callback')
def aera_callback():
    """Handle OAuth callback"""
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')
    
    if error:
        return jsonify({'error': f'Authorization failed: {error}'}), 400
    
    # Verify state
    saved_state = session.get('aera_state')
    if not state or not saved_state or state != saved_state:
        # Clear invalid state and redirect to home
        session.pop('aera_state', None)
        return redirect('/')
    
    if not code:
        return jsonify({'error': 'No authorization code'}), 400
    
    # Exchange code for token (handle ngrok HTTPS)
    scheme = request.headers.get('X-Forwarded-Proto', request.scheme)
    host = request.headers.get('X-Forwarded-Host', request.host)
    redirect_uri = f"{scheme}://{host}/auth/aera/callback"
    result = exchange_code(code, redirect_uri)
    
    if not result or 'access_token' not in result:
        print(f"[CALLBACK] Exchange failed or no access_token")
        return jsonify({'error': 'Token exchange failed'}), 500
    
    # Store token AND user data from token exchange
    # This is secure because:
    # 1. Token exchange requires client_secret (server-to-server)
    # 2. Data comes directly from AEra's API
    # 3. Stored in signed Flask session
    session[AERA_CONFIG['session_name']] = result['access_token']
    session['aera_user'] = {
        'wallet': result.get('wallet'),
        'score': result.get('score', 0),
        'has_nft': result.get('has_nft', False)
    }
    
    print(f"[CALLBACK] Token AND user data stored in session")
    print(f"[CALLBACK] User: {session['aera_user']}")
    
    # Clean up and redirect to protected area
    session.pop('aera_return_to', None)
    session.pop('aera_state', None)
    
    return redirect('/protected')


@app.route('/auth/aera/logout', methods=['POST'])
@csrf.exempt  # CSRF-Token im Frontend senden für echte Production
def aera_logout():
    """Logout user"""
    session.pop(AERA_CONFIG['session_name'], None)
    session.pop('aera_user', None)
    return jsonify({'success': True})


@app.route('/api/verify')
@limiter.limit("10 per minute")
def api_verify():
    """
    Verify current session with REAL TOKEN VERIFICATION
    Uses AEra's /api/v1/verify endpoint (FIXED on 22.12.2025)
    """
    # Get token from session
    token = session.get(AERA_CONFIG['session_name'])
    
    print(f"[VERIFY] ===== START VERIFY =====")
    print(f"[VERIFY] Token in session: {bool(token)}")
    
    if not token:
        print("[VERIFY] No token in session")
        return jsonify({'authenticated': False})
    
    # ✅ REAL TOKEN VERIFICATION with AEra API
    print(f"[VERIFY] Calling verify_token()...")
    user = verify_token(token)
    
    if not user:
        print("[VERIFY] Token verification failed - clearing session")
        session.pop(AERA_CONFIG['session_name'], None)
        session.pop('aera_user', None)
        return jsonify({'authenticated': False})
    
    print(f"[VERIFY] Token valid! User data: {user}")
    
    # Update session with fresh data from AEra
    session['aera_user'] = {
        'wallet': user.get('wallet'),
        'score': user.get('score', 0),
        'has_nft': user.get('has_nft', False)
    }
    
    # Check requirements
    if AERA_CONFIG['require_nft'] and not user.get('has_nft'):
        print(f"[VERIFY] NFT required but user has: {user.get('has_nft')}")
        return jsonify({
            'authenticated': False,
            'error': 'NFT required'
        })
    
    if AERA_CONFIG['min_score'] > 0 and user.get('score', 0) < AERA_CONFIG['min_score']:
        print(f"[VERIFY] Score too low: {user.get('score', 0)} < {AERA_CONFIG['min_score']}")
        return jsonify({
            'authenticated': False,
            'error': f'Minimum score of {AERA_CONFIG["min_score"]} required'
        })
    
    print(f"[VERIFY] ===== SUCCESS! User: {user.get('wallet')} =====")
    return jsonify({
        'authenticated': True,
        'user': {
            'wallet': user.get('wallet'),
            'score': user.get('score'),
            'has_nft': user.get('has_nft')
        }
    })


if __name__ == '__main__':
    # Check configuration
    if not AERA_CONFIG['client_id'] or not AERA_CONFIG['client_secret']:
        print("\n⚠️  WARNING: AERA_CLIENT_ID and AERA_CLIENT_SECRET not set!")
        print("Set them via environment variables or update AERA_CONFIG in server.py\n")
    
    print("\n🚀 AEra Gate Server starting...")
    print(f"📍 Base URL: {AERA_CONFIG['base_url']}")
    print(f"🔑 Client ID: {AERA_CONFIG['client_id'][:10]}..." if AERA_CONFIG['client_id'] else "🔑 Client ID: NOT SET")
    print("\n💡 Server will be available at:")
    print("   - http://localhost:8000")
    print("   - http://100.68.131.55:8000 (Tailscale)\n")
    
    app.run(host='0.0.0.0', port=8000, debug=True)
