#!/bin/bash

# ngrok Setup & Start Script for AEra Server
# Port: 8840

echo "🔧 ngrok Setup für AEra Server (Port 8840)"
echo ""
echo "WICHTIG: Du benötigst einen ngrok Auth Token!"
echo "1. Gehe zu: https://dashboard.ngrok.com/get-started/your-authtoken"
echo "2. Kopiere deinen Authtoken"
echo "3. Führe aus: ngrok config add-authtoken <dein_token>"
echo ""
read -p "Hast du ngrok bereits authentifiziert? (y/n): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    read -p "Gib deinen ngrok Authtoken ein: " NGROK_TOKEN
    ngrok config add-authtoken $NGROK_TOKEN
    echo "✓ ngrok authentifiziert"
fi

echo ""
echo "🚀 Starte ngrok für Port 8840..."
echo ""

# Starte ngrok im Hintergrund
nohup ngrok http 8840 --log=stdout > /var/www/aeralogin+implement/aeralogin/ngrok.log 2>&1 &
NGROK_PID=$!
echo $NGROK_PID > /var/www/aeralogin+implement/aeralogin/ngrok.pid

echo "✓ ngrok gestartet mit PID: $NGROK_PID"
echo "📝 Logs: /var/www/aeralogin+implement/aeralogin/ngrok.log"

# Warte kurz bis ngrok gestartet ist
sleep 3

# Hole ngrok URL
echo ""
echo "🌐 Deine öffentliche ngrok URL:"
curl -s http://localhost:4040/api/tunnels | grep -o 'https://[^"]*' | head -1

echo ""
echo ""
echo "📋 ngrok Management:"
echo "   • Dashboard: http://localhost:4040"
echo "   • Logs: tail -f /var/www/aeralogin+implement/aeralogin/ngrok.log"
echo "   • Stop: kill $(cat /var/www/aeralogin+implement/aeralogin/ngrok.pid)"
echo ""
