# AEra Identity & Resonance System

**AEra LogIn — Human-verified identity and on-chain resonance scoring on Coinbase's BASE L2.**

A Web3 authentication and reputation system built on Coinbase's BASE Layer 2 network, featuring Identity NFTs, Resonance Scores, and multi-platform follower tracking.

---

## 🌐 Built on BASE Sepolia

This project leverages **BASE Sepolia Testnet** (Chain ID: 84532) - Coinbase's Ethereum Layer 2 solution - for:

- **⚡ 99.97% Lower Gas Costs** - NFT minting ~$0.0003 vs $1.00 on Ethereum
- **🚀 Faster Transactions** - Sub-second confirmation times
- **🔗 EVM Compatible** - All Ethereum tools work seamlessly
- **🛡️ Ethereum Security** - Inherits Ethereum's security guarantees

### Network Information
- **Network**: BASE Sepolia Testnet
- **Chain ID**: 84532
- **RPC URL**: https://sepolia.base.org
- **Block Explorer**: https://sepolia.basescan.org

---

## 🎯 Features

### Identity System
- ✅ **Identity NFTs** - Soul-bound ERC-721 tokens for verified users
- ✅ **MetaMask Authentication** - Sign-in with Ethereum (EIP-4361)
- ✅ **Auto-Minting** - First-time users automatically receive Identity NFTs
- ✅ **Token ID Tracking** - Each user gets a unique, non-transferable NFT

### Reputation System (HYBRID Model)
- ✅ **Resonance Score** - On-chain reputation tracking (0-100+ scale)
- ✅ **Blockchain Sync** - Real-time score updates via milestone system (every 2 points)
- ✅ **HYBRID Score System** - Database-driven with pending_bonus mechanism
  - Follow Bonus: +2 pending points on follow
  - Login Activation: +1 base + pending bonus on creator login
  - Prevents double-minting while rewarding engagement
- ✅ **Score Evolution** - Dynamic scoring based on platform interactions
- ✅ **Transparent Verification** - All scores verifiable on-chain

### Social Features
- ✅ **Multi-Platform Tracking** - Twitter, Discord, Telegram, Direct links
- ✅ **Follower Dashboard** - Track verified followers and their scores
- ✅ **On-Chain Interactions** - All interactions recorded via recordInteraction()
  - FOLLOW interactions with weight=1 (contract validation compliant)
  - InteractionRecorded events emitted on blockchain
  - Complete interaction history queryable via events
- ✅ **Blockchain History Display** - Real-time interaction timeline with icons (👥📤💬🤝🏆)
- ✅ **Platform Integration** - Easy embedding with referral links

---

## 🏗️ Architecture

### Smart Contracts (BASE Sepolia)

| Contract | Address | Purpose | Explorer |
|---------|---------|---------|----------|
| **AEraIdentityNFT** | `0xF6f86cc0b916BCfE44cff64b00C2fe6e7954A3Ce` | Soul-bound Identity NFT | [View on Basescan](https://sepolia.basescan.org/address/0xF6f86cc0b916BCfE44cff64b00C2fe6e7954A3Ce) |
| **AEraResonanceScore** | `0xD4676a88bfAD40A87c8a5e889EE4AdD1448527c4` | On-chain reputation score | [View on Basescan](https://sepolia.basescan.org/address/0xD4676a88bfAD40A87c8a5e889EE4AdD1448527c4) |
| **AEraResonanceRegistry** | `0xE2d5B85E4A9B0820c59658607C03bC90ba63b7b9` | Interaction & follower log | [View on Basescan](https://sepolia.basescan.org/address/0xE2d5B85E4A9B0820c59658607C03bC90ba63b7b9) |

### Backend Components

- **FastAPI Server** (`server.py`) - REST API, dashboard backend & HYBRID score system
- **Web3 Service** (`web3_service.py`) - Full blockchain integration with all 3 smart contracts
  - Identity NFT minting & queries
  - Resonance Score updates (adminAdjust)
  - Interaction recording & history (recordInteraction)
- **Airdrop Worker** (`airdrop_worker.py`) - Background task processor
- **Logger** (`logger.py`) - Centralized logging system

---

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.9+ required
python --version

# Git and pip
sudo apt update
sudo apt install git python3-pip
```

### Installation

```bash
# Clone repository
git clone https://github.com/VEra-Resonance/AEra-LogIn-BASE-Sepolia.git
cd AEra-LogIn-BASE-Sepolia

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Required environment variables:

```env
# BASE Sepolia RPC
BASE_SEPOLIA_RPC_URL=https://sepolia.base.org

# Backend Wallet (with MINTER_ROLE)
PRIVATE_KEY=your_private_key_here

# Smart Contracts
IDENTITY_NFT_ADDRESS=0xF6f86cc0b916BCfE44cff64b00C2fe6e7954A3Ce
RESONANCE_SCORE_ADDRESS=0xD4676a88bfAD40A87c8a5e889EE4AdD1448527c4
RESONANCE_REGISTRY_ADDRESS=0xE2d5B85E4A9B0820c59658607C03bC90ba63b7b9

# Server
PORT=8840
```

### Start Server

```bash
# Development mode
source venv/bin/activate
python server.py
```

**Server will start on**: http://localhost:8840

---

## 📖 Usage

### For Users

1. **Visit Landing Page**: `http://localhost:8840`
2. **Connect MetaMask** - Ensure you're on BASE Sepolia network
3. **Sign Authentication** - Verify wallet ownership
4. **Receive Identity NFT** - Automatically minted on first login
5. **Access Dashboard** - View your followers and Resonance Score

### For Developers

#### API Endpoints

**Authentication:**
```bash
# Get challenge
GET /admin/challenge

# Verify signature
POST /admin/verify-signature
{
  "address": "0x...",
  "signature": "0x...",
  "message": "..."
}
```

**Identity NFT:**
```bash
# Check NFT status
GET /api/blockchain/identity/{address}

# Returns:
{
  "has_identity": true,
  "token_id": 15,
  "status": "active",
  "contract_address": "0xF6f86cc0b916BCfE44cff64b00C2fe6e7954A3Ce",
  "basescan_url": "https://sepolia.basescan.org/nft/..."
}
```

**Resonance Score:**
```bash
# Get score
GET /api/blockchain/score/{address}

# Returns:
{
  "db_score": 50,
  "blockchain_score": 50,
  "last_synced": "2025-12-01T10:30:00Z"
}
```

**Blockchain Interactions:**
```bash
# Get interaction history
GET /api/blockchain/interactions/{address}

# Returns:
{
  "interactions": [
    {
      "interaction_type": 0,
      "interaction_type_name": "FOLLOW",
      "initiator": "0x1234...",
      "responder": "0x5678...",
      "timestamp": 1733068883,
      "tx_hash": "0xabcd...",
      "block_number": 34417098
    }
  ],
  "total": 5
}
```

**Blockchain Stats:**
```bash
# Get blockchain health status
GET /api/blockchain/stats

# Returns:
{
  "identity_nft": "✅ Connected",
  "resonance_score": "✅ Connected",
  "resonance_registry": "✅ Connected",
  "backend_wallet": "0x22A2...",
  "network": "BASE Sepolia"
}
```

---

## 🔧 Development

### Project Structure

```
├── server.py                 # FastAPI backend (2800+ lines)
├── web3_service.py          # Blockchain integration (579 lines)
├── airdrop_worker.py        # Background tasks
├── logger.py                # Logging system
├── index.html               # Landing page
├── dashboard.html           # User dashboard with blockchain history
├── blockchain-dashboard.js  # Frontend blockchain interactions
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── .gitignore              # Security protection (extended)
└── backups/                 # Local backups (not in git)
```

### Technology Stack

- **Backend**: FastAPI, Python 3.9+
- **Blockchain**: Web3.py, eth-account
- **Frontend**: Vanilla JS, Web3.js, MetaMask
- **Database**: SQLite
- **Network**: BASE Sepolia (L2)

---

## 🛡️ Security

### What's Protected

✅ **Private keys never stored** - Only in `.env` (gitignored)  
✅ **Database excluded** - No user data in repository  
✅ **Logs excluded** - No sensitive information leaked  
✅ **Minimal data collection** - Only wallet addresses and scores  
✅ **EIP-4361 signatures** - Industry-standard authentication  
✅ **Dedicated system-role wallet** - AEra uses a dedicated system-role wallet for backend operations — no user keys are ever stored or processed

### Best Practices

1. **Never commit `.env` files**
2. **Keep private keys secure**
3. **Use testnet for development**
4. **Verify all contracts on Basescan**
5. **Regular security audits**

---

## 🌟 Why BASE Sepolia?

### Cost Comparison

| Operation | Ethereum Mainnet | BASE Sepolia | Savings |
|-----------|-----------------|--------------|---------|
| NFT Mint | ~$1.00 | ~$0.0003 | 99.97% |
| Score Update | ~$0.50 | ~$0.0002 | 99.96% |
| Registry Entry | ~$0.75 | ~$0.0002 | 99.97% |

### Technical Benefits

- **Ethereum Compatibility** - All Solidity contracts work without changes
- **Fast Finality** - Transactions confirm in seconds
- **Low Fees** - Enable micro-transactions and frequent updates
- **Coinbase Support** - Backed by major crypto exchange
- **Growing Ecosystem** - Active developer community

---

## 🛣️ Roadmap

- **Deploy contracts on BASE Mainnet** - Production-ready deployment
- **Dashboard V2 with cross-platform resonance analytics** - Enhanced user insights
- **Optional Miniapp integration** - Once SIWE is supported natively in Base Miniapps

---

## 📝 License

Apache License 2.0 - See [LICENSE](LICENSE) file for details

---

## 🔗 Links

- **Repository**: https://github.com/VEra-Resonance/AEra-LogIn-BASE-Sepolia
- **BASE Network**: https://base.org
- **BASE Sepolia Explorer**: https://sepolia.basescan.org
- **Coinbase L2 Docs**: https://docs.base.org

---

## 🤝 Contributing

This is an open-source project. Contributions are welcome!

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on BASE Sepolia
5. Submit a pull request

---

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Review smart contracts on Basescan
- Check BASE network status

---

**Built with ❤️ on BASE Sepolia - Coinbase's Ethereum L2 Solution**
