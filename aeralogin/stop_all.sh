#!/bin/bash

# AEra Complete Shutdown Script
# Stoppt Server + ngrok

cd /var/www/aeralogin+implement/aeralogin

echo "🛑 AEra LogIn - Complete Shutdown"
echo "=================================="
echo ""

# 1. Stop ngrok
echo "1️⃣ Stopping ngrok..."
if [ -f ngrok.pid ]; then
    NGROK_PID=$(cat ngrok.pid)
    kill $NGROK_PID 2>/dev/null && echo "   ✓ ngrok stopped (PID $NGROK_PID)" || echo "   ⚠️ ngrok process not found"
    rm -f ngrok.pid
else
    echo "   ⚠️ No ngrok PID file found"
fi

# Cleanup ngrok processes
pkill -f "ngrok http 8840" 2>/dev/null && echo "   ✓ Cleaned up ngrok processes"

echo ""

# 2. Stop Server
echo "2️⃣ Stopping Server..."
./stop_server.sh

echo ""
echo "=================================="
echo "✅ Shutdown Complete!"
echo ""
