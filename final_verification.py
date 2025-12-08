#!/usr/bin/env python3
import sqlite3
from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider("https://sepolia.base.org"))
score_address = "0xD4676a88bfAD40A87c8a5e889EE4AdD1448527c4"

abi = json.loads('[{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getResonance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')

contract = w3.eth.contract(address=score_address, abi=abi)

# Hole alle User aus DB
conn = sqlite3.connect("aera.db")
cursor = conn.cursor()
cursor.execute("SELECT address, score FROM users WHERE score > 0 ORDER BY score DESC, address")
users = cursor.fetchall()
conn.close()

print("🎯 FINALE SCORE VERIFICATION")
print("=" * 80)
print(f"Total Users: {len(users)}\n")

synced = 0
not_synced = 0
mismatch = 0

import time

for wallet, db_score in users:
    checksum = Web3.to_checksum_address(wallet)
    
    # Versuche mehrmals bei RPC-Caching-Problemen
    chain_score = 0
    for attempt in range(3):
        chain_score = contract.functions.getResonance(checksum).call()
        if chain_score > 0 or attempt == 2:
            break
        time.sleep(1)
    
    if chain_score == db_score:
        status = "✅"
        synced += 1
    elif chain_score == 0:
        status = "❌"
        not_synced += 1
    else:
        status = "⚠️"
        mismatch += 1
    
    print(f"{status} {wallet[:10]}... DB:{db_score:3d} → Chain:{chain_score:3d}")

print("\n" + "=" * 80)
print(f"📊 FINAL STATS:")
print(f"   ✅ Synced:      {synced}/{len(users)} ({synced*100//len(users)}%)")
print(f"   ❌ Not Synced:  {not_synced}/{len(users)}")
print(f"   ⚠️  Mismatch:    {mismatch}/{len(users)}")
print("=" * 80)
