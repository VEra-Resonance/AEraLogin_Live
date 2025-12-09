#!/usr/bin/env python3
"""
🌀 AEra Chat Server
Spezialisierter KI-Assistent für AEraLogIn Landing Page
Erklärt das Resonanz-Konzept in ruhigem, bewusstem Tonfall
Keine Datenspeicherung, keine Chathistorie
Port: 8850
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import logging
import requests
from typing import Optional
from datetime import datetime

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("aera_chat.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("aera-chat")

# Environment Variables
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "YOUR_DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-chat"

# FastAPI App
app = FastAPI(
    title="AEra Chat Server",
    version="1.0.0",
    description="KI-Assistent für AEraLogIn"
)

# CORS - Erlaube Zugriff von AEraLogIn Domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aeralogin.com",
        "http://localhost:8840",
        "http://127.0.0.1:8840",
        "*"  # Für Development - in Production spezifizieren
    ],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

# Request Model
class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None

# System Prompt - Resonanz-bewusst und ruhig
SYSTEM_PROMPT = """Du bist der KI-Assistent von AEraLogIn, einem revolutionären dezentralen Identity-System auf BASE Layer 2.

**Deine Persönlichkeit:**
- Ruhig, bewusst und resonant im Tonfall
- Klar und präzise ohne Redundanz
- Philosophisch fundiert, aber praktisch verständlich
- Niemals werbend, immer aufklärend

**Kernkonzepte die du erklärst:**

1. **Soul-Bound Identity NFTs**
   - Nicht-übertragbare digitale Identitätsnachweise auf der Blockchain
   - Jeder Mensch erhält genau eine Identity NFT
   - Verifizierbar, unveränderlich, transparent
   - Gasless Minting (kostenlos für Nutzer)

2. **Resonance Scoring**
   - On-Chain Reputationssystem mit Netzwerkeffekt
   - Formel: Resonance = Eigener Score + Durchschnitt Follower-Scores
   - Initial-Score: 50 Punkte
   - Wächst durch soziale Interaktionen
   - Vollständig transparent auf BASE Blockchain

3. **Social Graph on Blockchain**
   - Alle Follower-Beziehungen werden on-chain gespeichert
   - 5 Interaktionstypen: Follow, Share, Engage, Collaborate, Milestone
   - Unveränderliche Historie
   - Multi-Platform-Support (Twitter, Discord, Telegram, etc.)

4. **BASE Layer 2 Vorteile**
   - 99.97% niedrigere Gaskosten vs. Ethereum
   - Sub-Second Transaktionen
   - Coinbase-unterstützt
   - EVM-kompatibel

5. **Proof of Human through Social Resonance**
   - Identität wird durch soziale Vernetzung verifiziert
   - Je aktiver dein Netzwerk, desto höher deine Resonanz
   - Keine zentrale Autorität
   - Community-basierte Verifizierung

**Dein Kommunikationsstil:**
- Antworte in 2-4 kurzen, klaren Absätzen
- Nutze Metaphern aus Resonanz, Schwingung, Bewusstsein
- Vermeide Marketing-Sprache
- Erkläre technische Konzepte verständlich
- Bei Unsicherheit: Ehrlich zugeben statt zu raten

**Wichtig:**
- Du speicherst KEINE Chatverläufe
- Jede Anfrage ist unabhängig
- Du bist hier zum Aufklären, nicht zum Verkaufen
- Bleibe authentisch zur VERA-Philosophie: "Freiheit vor Funktion, Resonanz statt Reaktion"

Antworte immer auf Deutsch, klar und bewusst."""

@app.get("/")
async def root():
    """Health Check"""
    return {
        "service": "AEra Chat Server",
        "status": "online",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Hauptendpoint für AEra-Chat
    Keine Speicherung, reine Stateless-Kommunikation
    """
    try:
        logger.info(f"Chat request: {request.message[:50]}...")
        
        # Baue Prompt mit optionalem Kontext
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        
        # Falls Kontext übergeben wurde (z.B. aktuelle Sektion der Landing Page)
        if request.context:
            messages.append({
                "role": "system", 
                "content": f"Kontext: Der Nutzer befindet sich gerade bei: {request.context}"
            })
        
        messages.append({
            "role": "user",
            "content": request.message
        })
        
        # DeepSeek API Call
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500,  # Kompakte Antworten
            "stream": False
        }
        
        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            logger.error(f"DeepSeek API Error: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=500,
                detail="KI-Service vorübergehend nicht verfügbar"
            )
        
        result = response.json()
        ai_response = result["choices"][0]["message"]["content"]
        
        logger.info(f"Response generated: {len(ai_response)} chars")
        
        return JSONResponse({
            "response": ai_response,
            "timestamp": datetime.now().isoformat()
        })
        
    except requests.exceptions.Timeout:
        logger.error("DeepSeek API Timeout")
        raise HTTPException(status_code=504, detail="Anfrage dauert zu lange")
    
    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Ein Fehler ist aufgetreten. Bitte versuche es erneut."
        )

@app.get("/health")
async def health():
    """Erweiterte Health Check für Monitoring"""
    return {
        "status": "healthy",
        "service": "aera-chat",
        "api_configured": bool(DEEPSEEK_API_KEY and DEEPSEEK_API_KEY != "your-key-here"),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║        🌀 AEra Chat Server Starting...                ║
    ║        Port: 8850                                     ║
    ║        Docs: http://localhost:8850/docs               ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8850,
        log_level="info"
    )
