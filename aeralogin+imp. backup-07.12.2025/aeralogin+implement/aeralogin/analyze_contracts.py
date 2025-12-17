#!/usr/bin/env python3
"""
Analyse aller 3 Smart Contracts auf BASE Sepolia
"""
import os
from web3 import Web3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Web3 Setup
RPC_URL = "https://sepolia.base.org"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Contract Addresses
IDENTITY_NFT = "0xF6f86cc0b916BCfE44cff64b00C2fe6e7954A3Ce"
RESONANCE_SCORE = "0xD4676a88bfAD40A87c8a5e889EE4AdD1448527c4"
RESONANCE_REGISTRY = "0xE2d5B85E4A9B0820c59658607C03bC90ba63b7b9"

print("=" * 80)
print("📊 AERA SMART CONTRACTS - VOLLSTÄNDIGE ANALYSE")
print("=" * 80)
print(f"\n🌐 Verbunden mit: {RPC_URL}")
print(f"✅ Web3 Connected: {w3.is_connected()}")
print(f"📍 Current Block: {w3.eth.block_number:,}")

# Transfer Event Signature (für NFT Mints)
TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

print("\n" + "=" * 80)
print("1️⃣ IDENTITY NFT CONTRACT")
print("=" * 80)
print(f"📍 Address: {IDENTITY_NFT}")

try:
    # Get Transfer events (from 0x0 = mints)
    latest_block = w3.eth.block_number
    from_block = latest_block - 100000  # Last ~100k blocks
    
    print(f"🔍 Scanning blocks {from_block:,} → {latest_block:,}")
    
    logs = w3.eth.get_logs({
        'address': IDENTITY_NFT,
        'fromBlock': from_block,
        'toBlock': 'latest',
        'topics': [TRANSFER_TOPIC]
    })
    
    print(f"\n📊 Total Transfer Events: {len(logs)}")
    
    # Count mints (from = 0x0)
    mints = [log for log in logs if log['topics'][1] == b'\x00' * 32]
    print(f"🎨 NFTs Minted: {len(mints)}")
    
    if mints:
        # Get last mint
        last_mint = mints[-1]
        last_block_info = w3.eth.get_block(last_mint['blockNumber'])
        last_time = datetime.fromtimestamp(last_block_info['timestamp'])
        
        print(f"\n📅 Letzter Mint:")
        print(f"   Block: {last_mint['blockNumber']:,}")
        print(f"   Zeit: {last_time.strftime('%d.%m.%Y %H:%M:%S')}")
        print(f"   TX: {last_mint['transactionHash'].hex()}")
        
        # Decode token ID from topics[3]
        token_id = int.from_bytes(last_mint['topics'][3], byteorder='big')
        print(f"   Token ID: #{token_id}")
        
        # Get recipient from topics[2]
        recipient = '0x' + last_mint['topics'][2].hex()[-40:]
        print(f"   Empfänger: {recipient}")
    
    # Get all unique token holders
    recipients = set()
    for mint in mints:
        recipient = '0x' + mint['topics'][2].hex()[-40:]
        recipients.add(recipient)
    
    print(f"\n👥 Unique NFT Holders: {len(recipients)}")
    
except Exception as e:
    print(f"❌ Fehler: {e}")

print("\n" + "=" * 80)
print("2️⃣ RESONANCE SCORE CONTRACT")
print("=" * 80)
print(f"📍 Address: {RESONANCE_SCORE}")

try:
    # Get all events from Score Contract
    logs = w3.eth.get_logs({
        'address': RESONANCE_SCORE,
        'fromBlock': from_block,
        'toBlock': 'latest'
    })
    
    print(f"\n📊 Total Events: {len(logs)}")
    
    if logs:
        # Get last event
        last_event = logs[-1]
        last_block_info = w3.eth.get_block(last_event['blockNumber'])
        last_time = datetime.fromtimestamp(last_block_info['timestamp'])
        
        print(f"\n📅 Letzte Aktivität:")
        print(f"   Block: {last_event['blockNumber']:,}")
        print(f"   Zeit: {last_time.strftime('%d.%m.%Y %H:%M:%S')}")
        print(f"   TX: {last_event['transactionHash'].hex()}")
        
        # Count unique transactions
        unique_txs = set(log['transactionHash'] for log in logs)
        print(f"\n📈 Unique Transactions: {len(unique_txs)}")
        
except Exception as e:
    print(f"❌ Fehler: {e}")

print("\n" + "=" * 80)
print("3️⃣ RESONANCE REGISTRY CONTRACT")
print("=" * 80)
print(f"📍 Address: {RESONANCE_REGISTRY}")

try:
    # Get all events from Registry Contract
    logs = w3.eth.get_logs({
        'address': RESONANCE_REGISTRY,
        'fromBlock': from_block,
        'toBlock': 'latest'
    })
    
    print(f"\n📊 Total Events: {len(logs)}")
    
    if logs:
        # Get last event
        last_event = logs[-1]
        last_block_info = w3.eth.get_block(last_event['blockNumber'])
        last_time = datetime.fromtimestamp(last_block_info['timestamp'])
        
        print(f"\n📅 Letzte Aktivität:")
        print(f"   Block: {last_event['blockNumber']:,}")
        print(f"   Zeit: {last_time.strftime('%d.%m.%Y %H:%M:%S')}")
        print(f"   TX: {last_event['transactionHash'].hex()}")
        
        # Count unique transactions
        unique_txs = set(log['transactionHash'] for log in logs)
        print(f"\n📈 Unique Transactions: {len(unique_txs)}")
        
        # Try to identify InteractionRecorded events (4 topics)
        interaction_events = [log for log in logs if len(log['topics']) == 4]
        print(f"⛓️ InteractionRecorded Events: {len(interaction_events)}")
        
except Exception as e:
    print(f"❌ Fehler: {e}")

print("\n" + "=" * 80)
print("📊 GESAMTSTATISTIK")
print("=" * 80)

# Calculate total activity
total_nft_events = len(w3.eth.get_logs({
    'address': IDENTITY_NFT,
    'fromBlock': from_block,
    'toBlock': 'latest'
}))

total_score_events = len(w3.eth.get_logs({
    'address': RESONANCE_SCORE,
    'fromBlock': from_block,
    'toBlock': 'latest'
}))

total_registry_events = len(w3.eth.get_logs({
    'address': RESONANCE_REGISTRY,
    'fromBlock': from_block,
    'toBlock': 'latest'
}))

total_events = total_nft_events + total_score_events + total_registry_events

print(f"\n🎨 NFT Contract: {total_nft_events} events")
print(f"📊 Score Contract: {total_score_events} events")
print(f"⛓️ Registry Contract: {total_registry_events} events")
print(f"\n💫 TOTAL EVENTS: {total_events}")

print("\n" + "=" * 80)
print("✅ ANALYSE ABGESCHLOSSEN")
print("=" * 80)
