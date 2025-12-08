#!/bin/bash

# AEra Server Stop Script

cd /var/www/aeralogin+implement/aeralogin

if [ -f server_8840.pid ]; then
    PID=$(cat server_8840.pid)
    echo "🛑 Stopping server with PID $PID..."
    kill $PID 2>/dev/null && echo "✓ Server stopped" || echo "⚠️ Process not found"
    rm -f server_8840.pid
else
    echo "⚠️ No PID file found"
fi

# Cleanup any remaining Python processes on port 8840
lsof -ti:8840 | xargs kill -9 2>/dev/null && echo "✓ Cleaned up port 8840" || echo "ℹ️ Port 8840 already free"
