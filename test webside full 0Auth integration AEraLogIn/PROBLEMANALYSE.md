# OAuth-Server Problemanalyse & Lösungen

## 📊 Zusammenfassung

Der Test-OAuth-Server läuft jetzt unter `https://aeralogin.com/example-oauth/` parallel zum Hauptserver.

---

## ❌ Identifizierte Probleme

### 1. **JavaScript verwendete absolute Pfade ohne URL-Prefix**
```javascript
// ❌ VORHER (falsch):
const AERA_CONFIG = {
  loginPath: '/auth/aera/login',        // → 404 (fehlendes /example-oauth)
  verifyPath: '/api/verify'             // → 404
};
```

**Lösung:** Auto-Detection des URL-Prefix
```javascript
// ✅ NACHHER (korrekt):
const URL_PREFIX = window.location.pathname.split('/').slice(0, 2).join('/') || '';

const AERA_CONFIG = {
  loginPath: `${URL_PREFIX}/auth/aera/login`,     // → /example-oauth/auth/aera/login
  verifyPath: `${URL_PREFIX}/api/verify`          // → /example-oauth/api/verify
};
```

---

### 2. **Session-Cookie-Name `__Host-session` funktionierte nicht**
```python
# ❌ VORHER:
SESSION_COOKIE_NAME='__Host-session'  # Erfordert HTTPS direkt am Server
```

**Problem:** `__Host-` Cookies funktionieren nur bei direktem HTTPS, nicht über Reverse-Proxy.

**Lösung:**
```python
# ✅ NACHHER:
SESSION_COOKIE_NAME='aera_example_session',
SESSION_COOKIE_PATH=URL_PREFIX  # Scope auf /example-oauth
```

---

### 3. **Nginx-Konfiguration leitete Pfade falsch weiter**
```nginx
# ❌ VORHER:
location /example-oauth/static {
    proxy_pass http://127.0.0.1:8001/static;  # Entfernt /example-oauth!
}
```

**Problem:** Nginx entfernte den `/example-oauth` Prefix bei der Weiterleitung.

**Lösung:**
```nginx
# ✅ NACHHER:
location ~ ^/example-oauth(/.*)?$ {
    proxy_pass http://127.0.0.1:8001$request_uri;  # Behält kompletten Pfad
    proxy_set_header X-Forwarded-Proto $scheme;
    # ... weitere Headers
}
```

---

### 4. **Cloudflare cachte 404-Responses**
**Problem:** Alte 404-Responses wurden von Cloudflare gecacht.

**Lösung:**
- Cache-Buster Parameter verwenden (`?v=timestamp`)
- Cloudflare Purge Cache für `/example-oauth/*`
- Oder warten bis Cache abläuft

---

## ✅ Finale Konfiguration

### Server (Port 8001)
```python
URL_PREFIX = '/example-oauth'
PORT = 8001

app = Flask(__name__, static_url_path=f'{URL_PREFIX}/static')
app.config.update(
    SESSION_COOKIE_NAME='aera_example_session',
    SESSION_COOKIE_PATH=URL_PREFIX
)

@app.route(f'{URL_PREFIX}/')
def index():
    return send_from_directory('.', 'index.html')
```

### Nginx (aeralogin.conf)
```nginx
# Example OAuth Test Server
location ~ ^/example-oauth(/.*)?$ {
    proxy_pass http://127.0.0.1:8001$request_uri;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# Main Server (unverändert)
location / {
    proxy_pass http://127.0.0.1:8840;
}
```

### Frontend (aera-client.js)
```javascript
// Auto-detect URL prefix
const URL_PREFIX = window.location.pathname.split('/').slice(0, 2).join('/') || '';

const AERA_CONFIG = {
  loginPath: `${URL_PREFIX}/auth/aera/login`,
  logoutPath: `${URL_PREFIX}/auth/aera/logout`,
  verifyPath: `${URL_PREFIX}/api/verify`
};
```

---

## 🎯 Verfügbare Endpunkte

✅ **Startseite:** `https://aeralogin.com/example-oauth/`  
✅ **Login:** `https://aeralogin.com/example-oauth/auth/aera/login`  
✅ **OAuth Callback:** `https://aeralogin.com/example-oauth/auth/aera/callback`  
✅ **API Verify:** `https://aeralogin.com/example-oauth/api/verify`  
✅ **Protected:** `https://aeralogin.com/example-oauth/protected`  
✅ **Static Files:** `https://aeralogin.com/example-oauth/static/aera-client.js`

---

## 🔧 Nächste Schritte

1. ✅ Server läuft auf Port 8001
2. ✅ Nginx-Routing konfiguriert
3. ✅ URL-Prefix Auto-Detection implementiert
4. ✅ Session-Cookies korrekt konfiguriert
5. ⏳ **Cloudflare Cache clearen** (oder warten)
6. ⏳ **OAuth-Flow testen** mit echtem Login

---

## 📝 Hinweise

- **Hauptserver bleibt unverändert** auf Port 8840
- **Testserver parallel** auf Port 8001
- **Kein Konflikt** zwischen beiden Servern
- **Sessions sind getrennt** durch unterschiedliche Cookie-Namen und Paths
- **Cloudflare Cache** kann alte Responses zwischenspeichern → Cache-Buster verwenden

---

Erstellt: 2025-12-24  
Status: ✅ Funktionsfähig (mit Cloudflare Cache-Warnung)
