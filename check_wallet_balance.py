from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

rpc_url = "https://sepolia.base.org"
wallet = "0xed1a95ab5b794Dc20964693FBCc60A3DFb5A22C5"

w3 = Web3(Web3.HTTPProvider(rpc_url))

if w3.is_connected():
    balance_wei = w3.eth.get_balance(wallet)
    balance_eth = w3.from_wei(balance_wei, 'ether')
    
    print(f"🔍 WALLET BALANCE CHECK:")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"�� Wallet: {wallet}")
    print(f"💰 Balance (Wei): {balance_wei}")
    print(f"💰 Balance (ETH): {balance_eth}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    if balance_wei > 0:
        gas_price = w3.eth.gas_price
        estimated_gas = 100000  # NFT mint cost
        tx_cost_wei = gas_price * estimated_gas
        tx_cost_eth = w3.from_wei(tx_cost_wei, 'ether')
        possible_mints = int(balance_wei / tx_cost_wei) if tx_cost_wei > 0 else 0
        
        print(f"⛽ Current Gas Price: {w3.from_wei(gas_price, 'gwei')} gwei")
        print(f"📊 Estimated TX Cost: {tx_cost_eth} ETH")
        print(f"🎨 Possible NFT Mints: ~{possible_mints}")
        print(f"✅ READY TO MINT!" if balance_wei > tx_cost_wei else "⚠️ BALANCE TOO LOW")
    else:
        print(f"❌ WALLET IS EMPTY - NEEDS FUNDING!")
else:
    print("❌ RPC CONNECTION FAILED")
