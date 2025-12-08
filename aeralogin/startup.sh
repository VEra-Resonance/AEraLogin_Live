#!/bin/bash

# AEra Complete Startup Script
# Startet Server + ngrok für Port 8840

cd /var/www/aeralogin+implement/aeralogin

echo "🚀 AEra LogIn - Complete Startup"
echo "================================"
echo ""

# 1. Starte Server
echo "1️⃣ Starting Server on Port 8840..."
./start_server.sh
sleep 2

# 2. Überprüfe ob Server läuft
if lsof -i:8840 > /dev/null 2>&1; then
    echo "   ✓ Server is running on Port 8840"
else
    echo "   ❌ Server failed to start!"
    exit 1
fi

echo ""

# 3. Starte ngrok
echo "2️⃣ Starting ngrok tunnel..."
if [ -f ngrok.pid ] && ps -p $(cat ngrok.pid) > /dev/null 2>&1; then
    echo "   ⚠️ ngrok already running"
else
    nohup ngrok http 8840 --log=stdout > ngrok.log 2>&1 &
    echo $! > ngrok.pid
    echo "   ✓ ngrok started with PID $(cat ngrok.pid)"
fi

sleep 3

echo ""
echo "================================"
echo "✅ Startup Complete!"
echo ""
echo "📊 Status:"
echo "   • Server: http://localhost:8840"
echo "   • ngrok Dashboard: http://localhost:4040"
echo ""

# Zeige ngrok URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -o 'https://[^"]*ngrok[^"]*' | head -1)
if [ -n "$NGROK_URL" ]; then
    echo "🌐 Public URL: $NGROK_URL"
    echo ""
    echo "💡 Update .env with: NGROK_URL=$NGROK_URL"
else
    echo "⚠️ Could not fetch ngrok URL (wait a few seconds and check http://localhost:4040)"
fi

echo ""
echo "📝 Logs:"
echo "   • Server: tail -f server_8840.log"
echo "   • ngrok: tail -f ngrok.log"
echo ""
echo "🛑 Stop all: ./stop_all.sh"
echo ""
