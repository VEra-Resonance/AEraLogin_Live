#!/bin/bash

# AEra Server Start Script
# Port: 8840

cd /var/www/aeralogin+implement/aeralogin

# Aktiviere Virtual Environment falls vorhanden
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "../venv" ]; then
    source ../venv/bin/activate
fi

# Starte Server
echo "🚀 Starting AEra Server on Port 8840..."
python3 server.py > server_8840.log 2>&1 &

# Speichere PID
echo $! > server_8840.pid
echo "✓ Server started with PID $(cat server_8840.pid)"
echo "📝 Logs: server_8840.log"
echo "🌐 URL: http://localhost:8840"
