#!/usr/bin/env python3
"""
Grant DEFAULT_ADMIN_ROLE to Safe Wallet for AEra Profile NFT Contract
======================================================================

This script adds the Safe Wallet as an additional admin WITHOUT removing
any existing roles from the Backend wallet.

Contract: 0x0a630A3Dc0C7387e0226D1b285C43B753506b27E (AEra Profile NFT)
Current Admin: 0x22A2cAcB19e77D25DA063A787870A3eE6BAC8Dfe (Backend)
New Admin: 0xC8B1bEb43361bb78400071129139A37Eb5c5Dd93 (Safe Wallet)

The Backend wallet keeps all its roles (DEFAULT_ADMIN_ROLE, MINTER_ROLE, etc.)
"""

import os
import sys
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account

# Load .env file
load_dotenv()

# ========================================
# CONFIGURATION
# ========================================
ALCHEMY_URL = "https://base-mainnet.g.alchemy.com/v2/u_oAA5oIIbGQ-0AdX3efg"
CHAIN_ID = 8453  # BASE Mainnet

# Contract address
PROFILE_NFT_CONTRACT = "0x0a630A3Dc0C7387e0226D1b285C43B753506b27E"

# Addresses
BACKEND_WALLET = "0x22A2cAcB19e77D25DA063A787870A3eE6BAC8Dfe"
SAFE_WALLET = "0xC8B1bEb43361bb78400071129139A37Eb5c5Dd93"

# Role constants
DEFAULT_ADMIN_ROLE = bytes(32)  # 0x0000...0000

# Minimal ABI for AccessControl
ACCESS_CONTROL_ABI = [
    {
        "inputs": [
            {"internalType": "bytes32", "name": "role", "type": "bytes32"},
            {"internalType": "address", "name": "account", "type": "address"}
        ],
        "name": "grantRole",
        "outputs": [],
        "stateMutability": "nonpayable",
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
    }
]

def main():
    print("=" * 60)
    print("🔐 Grant DEFAULT_ADMIN_ROLE to Safe Wallet")
    print("=" * 60)
    print()
    
    # Get private key from environment
    private_key = os.environ.get("BACKEND_PRIVATE_KEY")
    if not private_key:
        print("❌ ERROR: BACKEND_PRIVATE_KEY environment variable not set!")
        print()
        print("Usage:")
        print("  export BACKEND_PRIVATE_KEY='your_private_key_here'")
        print("  python3 grant_admin_to_safe.py")
        sys.exit(1)
    
    # Connect to BASE Mainnet
    print("🔗 Connecting to BASE Mainnet...")
    w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
    
    if not w3.is_connected():
        print("❌ Failed to connect to BASE Mainnet!")
        sys.exit(1)
    
    print(f"✅ Connected! Block: {w3.eth.block_number}")
    print()
    
    # Load account
    account = Account.from_key(private_key)
    print(f"📍 Sender Wallet: {account.address}")
    
    # Verify sender is the backend wallet
    if account.address.lower() != BACKEND_WALLET.lower():
        print(f"⚠️  WARNING: Sender address doesn't match expected Backend wallet!")
        print(f"   Expected: {BACKEND_WALLET}")
        print(f"   Got:      {account.address}")
        response = input("Continue anyway? (yes/no): ")
        if response.lower() != "yes":
            print("Aborted.")
            sys.exit(0)
    
    # Create contract instance
    contract = w3.eth.contract(
        address=Web3.to_checksum_address(PROFILE_NFT_CONTRACT),
        abi=ACCESS_CONTROL_ABI
    )
    
    # Check if Safe already has admin role
    print()
    print("🔍 Checking current roles...")
    
    safe_has_admin = contract.functions.hasRole(DEFAULT_ADMIN_ROLE, SAFE_WALLET).call()
    backend_has_admin = contract.functions.hasRole(DEFAULT_ADMIN_ROLE, BACKEND_WALLET).call()
    
    print(f"   Backend has DEFAULT_ADMIN_ROLE: {'✅ YES' if backend_has_admin else '❌ NO'}")
    print(f"   Safe has DEFAULT_ADMIN_ROLE:    {'✅ YES' if safe_has_admin else '❌ NO'}")
    
    if safe_has_admin:
        print()
        print("✅ Safe Wallet already has DEFAULT_ADMIN_ROLE!")
        print("   No action needed.")
        sys.exit(0)
    
    if not backend_has_admin:
        print()
        print("❌ ERROR: Backend wallet doesn't have DEFAULT_ADMIN_ROLE!")
        print("   Cannot grant role without admin privileges.")
        sys.exit(1)
    
    # Confirm action
    print()
    print("=" * 60)
    print("📋 TRANSACTION DETAILS")
    print("=" * 60)
    print(f"   Contract:  {PROFILE_NFT_CONTRACT}")
    print(f"   Function:  grantRole(DEFAULT_ADMIN_ROLE, Safe)")
    print(f"   Safe:      {SAFE_WALLET}")
    print()
    print("⚠️  This will add the Safe Wallet as an additional admin.")
    print("   The Backend wallet keeps all its existing roles!")
    print()
    
    response = input("Execute transaction? (yes/no): ")
    if response.lower() != "yes":
        print("Aborted.")
        sys.exit(0)
    
    # Build transaction
    print()
    print("🔨 Building transaction...")
    
    nonce = w3.eth.get_transaction_count(account.address)
    gas_price = w3.eth.gas_price
    
    tx = contract.functions.grantRole(
        DEFAULT_ADMIN_ROLE,
        Web3.to_checksum_address(SAFE_WALLET)
    ).build_transaction({
        'chainId': CHAIN_ID,
        'gas': 100000,
        'gasPrice': gas_price,
        'nonce': nonce,
    })
    
    # Estimate gas
    try:
        estimated_gas = w3.eth.estimate_gas(tx)
        tx['gas'] = int(estimated_gas * 1.2)  # 20% buffer
        print(f"   Estimated gas: {estimated_gas}")
    except Exception as e:
        print(f"⚠️  Gas estimation failed: {e}")
        print("   Using default gas: 100000")
    
    gas_cost_wei = tx['gas'] * gas_price
    gas_cost_eth = w3.from_wei(gas_cost_wei, 'ether')
    print(f"   Gas price: {w3.from_wei(gas_price, 'gwei'):.2f} Gwei")
    print(f"   Max cost: ~{gas_cost_eth:.6f} ETH")
    
    # Sign transaction
    print()
    print("✍️  Signing transaction...")
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    
    # Send transaction
    print("📤 Sending transaction...")
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"   TX Hash: {tx_hash.hex()}")
    print(f"   BaseScan: https://basescan.org/tx/{tx_hash.hex()}")
    
    # Wait for confirmation
    print()
    print("⏳ Waiting for confirmation...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    
    if receipt.status == 1:
        print()
        print("=" * 60)
        print("✅ SUCCESS! DEFAULT_ADMIN_ROLE granted to Safe Wallet!")
        print("=" * 60)
        print(f"   TX Hash: {tx_hash.hex()}")
        print(f"   Gas Used: {receipt.gasUsed}")
        print()
        
        # Verify
        safe_has_admin_now = contract.functions.hasRole(DEFAULT_ADMIN_ROLE, SAFE_WALLET).call()
        backend_has_admin_now = contract.functions.hasRole(DEFAULT_ADMIN_ROLE, BACKEND_WALLET).call()
        
        print("🔍 Verification:")
        print(f"   Backend has DEFAULT_ADMIN_ROLE: {'✅ YES' if backend_has_admin_now else '❌ NO'}")
        print(f"   Safe has DEFAULT_ADMIN_ROLE:    {'✅ YES' if safe_has_admin_now else '❌ NO'}")
        
    else:
        print()
        print("❌ Transaction FAILED!")
        print(f"   Receipt: {receipt}")
        sys.exit(1)


if __name__ == "__main__":
    main()
