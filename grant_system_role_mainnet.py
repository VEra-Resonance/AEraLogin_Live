#!/usr/bin/env python3
"""
Grant SYSTEM_ROLE to Backend Wallet on Registry Contract
"""
import os
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("BASE_SEPOLIA_RPC_URL")
CHAIN_ID = int(os.getenv("BASE_NETWORK_CHAIN_ID"))

# Use Backend Wallet (has DEFAULT_ADMIN_ROLE as deployer)
ADMIN_ADDRESS = os.getenv("BACKEND_ADDRESS")
ADMIN_PRIVATE_KEY = os.getenv("BACKEND_PRIVATE_KEY")

# Backend Wallet needs SYSTEM_ROLE
BACKEND_ADDRESS = os.getenv("BACKEND_ADDRESS")

# Registry Contract
REGISTRY_ADDRESS = os.getenv("REGISTRY_ADDRESS")

# Role hash
SYSTEM_ROLE = Web3.keccak(text="SYSTEM_ROLE")

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = Account.from_key(ADMIN_PRIVATE_KEY)

ACCESS_CONTROL_ABI = [
    {
        "inputs": [{"name": "role", "type": "bytes32"}, {"name": "account", "type": "address"}],
        "name": "grantRole",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "role", "type": "bytes32"}, {"name": "account", "type": "address"}],
        "name": "hasRole",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

print("=" * 80)
print("🔑 GRANT SYSTEM_ROLE TO BACKEND WALLET")
print("=" * 80)
print(f"\n📍 Registry: {REGISTRY_ADDRESS}")
print(f"👤 Admin: {ADMIN_ADDRESS}")
print(f"🤖 Backend: {BACKEND_ADDRESS}")
print(f"💰 Admin Balance: {w3.from_wei(w3.eth.get_balance(ADMIN_ADDRESS), 'ether'):.6f} ETH")

contract = w3.eth.contract(
    address=Web3.to_checksum_address(REGISTRY_ADDRESS),
    abi=ACCESS_CONTROL_ABI
)

# Check current status
has_role = contract.functions.hasRole(SYSTEM_ROLE, BACKEND_ADDRESS).call()
print(f"\n🔍 Backend Wallet has SYSTEM_ROLE: {' ✅ YES' if has_role else '❌ NO'}")

if has_role:
    print("\n✅ Backend Wallet already has SYSTEM_ROLE!")
    print("   recordInteraction() should work now.")
    exit(0)

print("\n🔄 Granting SYSTEM_ROLE...")

try:
    nonce = w3.eth.get_transaction_count(ADMIN_ADDRESS)
    gas_price = w3.eth.gas_price
    
    tx = contract.functions.grantRole(SYSTEM_ROLE, BACKEND_ADDRESS).build_transaction({
        'from': ADMIN_ADDRESS,
        'nonce': nonce,
        'gas': 100000,
        'maxFeePerGas': gas_price * 2,
        'maxPriorityFeePerGas': gas_price,
        'chainId': CHAIN_ID
    })
    
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    print(f"📤 TX sent: {tx_hash.hex()}")
    print(f"🔗 Basescan: https://basescan.org/tx/{tx_hash.hex()}")
    print(f"⏳ Waiting for confirmation...")
    
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    
    if receipt['status'] == 1:
        print(f"✅ SUCCESS!")
        print(f"   Gas used: {receipt['gasUsed']}")
        print(f"\n🎉 Backend Wallet now has SYSTEM_ROLE!")
        print(f"   recordInteraction() will now work on-chain!")
    else:
        print(f"❌ FAILED - Transaction reverted")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
