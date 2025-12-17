"""
🔑 Grant SYSTEM_ROLE für recordInteraction()
"""

import asyncio
import os
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv

load_dotenv()

# Configuration
RPC_URL = "https://sepolia.base.org"
REGISTRY_ADDRESS = "0xE2d5B85E4A9B0820c59658607C03bC90ba63b7b9"
BACKEND_WALLET = "0x22A2cAcB19e77D25DA063A787870A3eE6BAC8Dfe"

# Private Key (muss DEFAULT_ADMIN_ROLE haben!)
PRIVATE_KEY = os.getenv("BACKEND_PRIVATE_KEY")
if not PRIVATE_KEY:
    print("❌ BACKEND_PRIVATE_KEY nicht in .env gefunden!")
    exit(1)

if not PRIVATE_KEY.startswith('0x'):
    PRIVATE_KEY = '0x' + PRIVATE_KEY

print("=" * 80)
print("🔑 SYSTEM_ROLE GRANT")
print("=" * 80)

# Web3 Setup
w3 = Web3(Web3.HTTPProvider(RPC_URL))
if not w3.is_connected():
    print("❌ Keine Verbindung zu BASE Sepolia!")
    exit(1)

print(f"\n✅ Verbunden mit BASE Sepolia")
print(f"📍 Registry Contract: {REGISTRY_ADDRESS}")
print(f"👤 Backend Wallet: {BACKEND_WALLET}")

# Account
account = Account.from_key(PRIVATE_KEY)
print(f"🔐 Signing Account: {account.address}")

# Registry Contract ABI (nur benötigte Funktionen)
REGISTRY_ABI = [
    {
        "inputs": [],
        "name": "DEFAULT_ADMIN_ROLE",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "role", "type": "bytes32"},
            {"internalType": "address", "name": "account", "type": "address"}
        ],
        "name": "hasRole",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "role", "type": "bytes32"},
            {"internalType": "address", "name": "account", "type": "address"}
        ],
        "name": "grantRole",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

registry = w3.eth.contract(address=REGISTRY_ADDRESS, abi=REGISTRY_ABI)

# SYSTEM_ROLE berechnen
SYSTEM_ROLE = w3.keccak(text="SYSTEM_ROLE")
print(f"\n🔑 SYSTEM_ROLE: {SYSTEM_ROLE.hex()}")

# Check if already has role
print(f"\n⏳ Prüfe aktuelle Rollen...")
has_system_role = registry.functions.hasRole(SYSTEM_ROLE, BACKEND_WALLET).call()
print(f"   SYSTEM_ROLE: {'✅ AKTIV' if has_system_role else '❌ FEHLT'}")

if has_system_role:
    print("\n✅ SYSTEM_ROLE bereits vergeben!")
    print("   → recordInteraction() sollte jetzt funktionieren!")
    exit(0)

# Check if we have DEFAULT_ADMIN_ROLE
DEFAULT_ADMIN_ROLE = registry.functions.DEFAULT_ADMIN_ROLE().call()
has_admin = registry.functions.hasRole(DEFAULT_ADMIN_ROLE, account.address).call()

if not has_admin:
    print(f"\n❌ Account {account.address} hat keine DEFAULT_ADMIN_ROLE!")
    print("   → Kann SYSTEM_ROLE nicht vergeben!")
    exit(1)

print(f"\n✅ Account hat DEFAULT_ADMIN_ROLE")
print(f"\n⏳ Grant SYSTEM_ROLE an {BACKEND_WALLET}...")

try:
    # Build transaction
    nonce = w3.eth.get_transaction_count(account.address)
    
    grant_tx = registry.functions.grantRole(
        SYSTEM_ROLE,
        BACKEND_WALLET
    ).build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': 100000,
        'maxFeePerGas': w3.eth.gas_price * 2,
        'maxPriorityFeePerGas': w3.to_wei('0.1', 'gwei'),
        'chainId': 84532
    })
    
    # Sign & send
    signed = account.sign_transaction(grant_tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    
    print(f"📤 Transaction gesendet: {tx_hash.hex()}")
    print(f"⏳ Warte auf Bestätigung...")
    
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    
    if receipt['status'] == 1:
        print(f"\n✅ SYSTEM_ROLE erfolgreich vergeben!")
        print(f"   TX: {tx_hash.hex()}")
        print(f"   Block: {receipt['blockNumber']}")
        print(f"   Gas: {receipt['gasUsed']}")
        
        # Verify
        has_role_now = registry.functions.hasRole(SYSTEM_ROLE, BACKEND_WALLET).call()
        if has_role_now:
            print(f"\n✅ VERIFICATION: SYSTEM_ROLE ist aktiv!")
            print(f"\n🎯 NÄCHSTER SCHRITT:")
            print(f"   → Teste recordInteraction() erneut!")
            print(f"   → Sollte jetzt funktionieren!")
        else:
            print(f"\n⚠️  Role grant succeeded but verification failed?!")
    else:
        print(f"\n❌ Transaction FAILED!")
        print(f"   TX: {tx_hash.hex()}")
        
except Exception as e:
    print(f"\n❌ Fehler: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)

