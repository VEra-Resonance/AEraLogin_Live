#!/usr/bin/env python3
"""Bulk Score Sync - Alle User-Scores auf Blockchain synchronisieren"""
import sqlite3
from web3 import Web3
from dotenv import load_dotenv
import os
import json
import time
from datetime import datetime

load_dotenv()

# Setup
rpc_url = "https://sepolia.base.org"
score_address = "0xD4676a88bfAD40A87c8a5e889EE4AdD1448527c4"
backend_key = os.getenv("BACKEND_PRIVATE_KEY")
db_path = "aera.db"

w3 = Web3(Web3.HTTPProvider(rpc_url))
account = w3.eth.account.from_key(backend_key)

# ABI mit adminAdjust und getResonance
abi = json.loads('[{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"newAmount","type":"uint256"}],"name":"adminAdjust","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getResonance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')

contract = w3.eth.contract(address=score_address, abi=abi)

print("🚀 BULK SCORE SYNC - ALLE USER")
print("=" * 80)
print(f"⏰ Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"📊 Contract: {score_address}")
print(f"💼 Backend:  {account.address}")
print(f"💰 Balance:  {w3.eth.get_balance(account.address) / 1e18:.6f} ETH")
print("=" * 80)

# Hole alle User aus DB
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT address, score FROM users WHERE score > 0 ORDER BY address")
users = cursor.fetchall()
conn.close()

print(f"\n📋 Gefunden: {len(users)} User in Datenbank\n")

# Statistiken
stats = {
    'total': len(users),
    'success': 0,
    'failed': 0,
    'skipped': 0,
    'gas_used': 0,
    'eth_spent': 0
}

results = []

# Prozessiere jeden User
for idx, (wallet, db_score) in enumerate(users, 1):
    print(f"\n{'─' * 80}")
    print(f"[{idx}/{len(users)}] 👤 {wallet}")
    print(f"    📊 DB Score: {db_score}")
    
    try:
        # Prüfe aktuellen Blockchain-Score
        checksum_addr = Web3.to_checksum_address(wallet)
        current_score = contract.functions.getResonance(checksum_addr).call()
        print(f"    ⛓️  Chain Score: {current_score}")
        
        # Skip wenn Score bereits korrekt ist
        if current_score == db_score:
            print(f"    ⏭️  SKIP - Score bereits synchronisiert")
            stats['skipped'] += 1
            results.append({
                'wallet': wallet,
                'status': 'skipped',
                'db_score': db_score,
                'chain_score': current_score
            })
            continue
        
        # adminAdjust Transaction bauen
        nonce = w3.eth.get_transaction_count(account.address)
        tx = contract.functions.adminAdjust(checksum_addr, db_score).build_transaction({
            'from': account.address,
            'nonce': nonce,
            'gas': 150000,
            'gasPrice': w3.eth.gas_price,
        })
        
        # Signieren und senden
        signed_tx = w3.eth.account.sign_transaction(tx, backend_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        print(f"    📤 TX: {tx_hash.hex()}")
        print(f"    ⏳ Warte auf Bestätigung...", end='', flush=True)
        
        # Warte auf Receipt
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        
        if receipt['status'] == 1:
            gas_used = receipt['gasUsed']
            eth_spent = gas_used * tx['gasPrice'] / 1e18
            stats['gas_used'] += gas_used
            stats['eth_spent'] += eth_spent
            
            print(f" ✅ SUCCESS!")
            print(f"    ⛽ Gas: {gas_used:,} (~{eth_spent:.6f} ETH)")
            print(f"    🔗 https://sepolia.basescan.org/tx/{tx_hash.hex()}")
            
            # Verify neuer Score
            new_score = contract.functions.getResonance(checksum_addr).call()
            if new_score == db_score:
                print(f"    ✅ Score verified: {new_score}")
                stats['success'] += 1
                results.append({
                    'wallet': wallet,
                    'status': 'success',
                    'db_score': db_score,
                    'chain_score': new_score,
                    'tx_hash': tx_hash.hex(),
                    'gas_used': gas_used
                })
            else:
                print(f"    ⚠️  Score mismatch: expected {db_score}, got {new_score}")
                stats['failed'] += 1
                results.append({
                    'wallet': wallet,
                    'status': 'mismatch',
                    'db_score': db_score,
                    'chain_score': new_score,
                    'tx_hash': tx_hash.hex()
                })
        else:
            print(f" ❌ FAILED!")
            stats['failed'] += 1
            results.append({
                'wallet': wallet,
                'status': 'tx_failed',
                'db_score': db_score,
                'tx_hash': tx_hash.hex()
            })
        
        # Kleine Pause zwischen Transactions
        if idx < len(users):
            time.sleep(2)
            
    except Exception as e:
        print(f"    ❌ Error: {str(e)[:100]}")
        stats['failed'] += 1
        results.append({
            'wallet': wallet,
            'status': 'error',
            'db_score': db_score,
            'error': str(e)[:200]
        })

# Final Report
print("\n" + "=" * 80)
print("📊 BULK SYNC - FINAL REPORT")
print("=" * 80)
print(f"⏰ Ende: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\n📈 STATISTIK:")
print(f"   Total User:     {stats['total']}")
print(f"   ✅ Success:     {stats['success']}")
print(f"   ⏭️  Skipped:     {stats['skipped']} (bereits synchronisiert)")
print(f"   ❌ Failed:      {stats['failed']}")
print(f"\n⛽ GAS & KOSTEN:")
print(f"   Total Gas:      {stats['gas_used']:,}")
print(f"   Total ETH:      {stats['eth_spent']:.6f} ETH")
print(f"   Avg Gas/TX:     {stats['gas_used'] // max(stats['success'], 1):,}")

# Backend Balance nach Sync
final_balance = w3.eth.get_balance(account.address) / 1e18
print(f"\n💰 BACKEND WALLET:")
print(f"   Vorher:         0.019956 ETH")
print(f"   Nachher:        {final_balance:.6f} ETH")
print(f"   Verbraucht:     {0.019956 - final_balance:.6f} ETH")

# Failed/Error Details
if stats['failed'] > 0:
    print(f"\n❌ FEHLGESCHLAGENE TRANSACTIONS:")
    for r in results:
        if r['status'] in ['tx_failed', 'error', 'mismatch']:
            print(f"   {r['wallet'][:10]}... - {r['status']}")
            if 'error' in r:
                print(f"      Error: {r['error'][:100]}")

print("\n" + "=" * 80)

# Speichere Report
report_file = f"bulk_sync_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(report_file, 'w') as f:
    json.dump({
        'timestamp': datetime.now().isoformat(),
        'stats': stats,
        'results': results
    }, f, indent=2)

print(f"📝 Report gespeichert: {report_file}")
print("=" * 80)

