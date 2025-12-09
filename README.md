# AEra Identity & Resonance System

**AEra LogIn — Human-verified identity and on-chain resonance scoring on Coinbase's BASE L2.**

A Web3 authentication and reputation system built on Coinbase's BASE Layer 2 network, featuring Identity NFTs, Resonance Scores, and multi-platform follower tracking.

---

## 🌐 Live on BASE Mainnet

This project is deployed on **BASE Mainnet** (Chain ID: 8453) - Coinbase's Ethereum Layer 2 solution - for:

- **⚡ 99.97% Lower Gas Costs** - NFT minting ~$0.0003 vs $1.00 on Ethereum
- **🚀 Faster Transactions** - Sub-second confirmation times
- **🔗 EVM Compatible** - All Ethereum tools work seamlessly
- **🛡️ Ethereum Security** - Inherits Ethereum's security guarantees

### Network Information
- **Network**: BASE Mainnet
- **Chain ID**: 8453
- **RPC URL**: https://mainnet.base.org
- **Block Explorer**: https://basescan.org

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

### Smart Contracts (BASE Mainnet)

| Contract | Address | Purpose | Explorer |
|---------|---------|---------|----------|
| **AEraIdentityNFT** | `0xF9ff5DC523927B9632049bd19e17B610E9197d53` | Soul-bound Identity NFT | [View on Basescan](https://basescan.org/address/0xF9ff5DC523927B9632049bd19e17B610E9197d53) |
| **AEraResonanceScore** | `0x9A814DBF7E2352CE9eA6293b4b731B2a24800102` | On-chain reputation score | [View on Basescan](https://basescan.org/address/0x9A814DBF7E2352CE9eA6293b4b731B2a24800102) |
| **AEraResonanceRegistry** | `0xAAf30d96382D2409Cf1626095e97BEc1C59e5cdF` | Interaction & follower log | [View on Basescan](https://basescan.org/address/0xAAf30d96382D2409Cf1626095e97BEc1C59e5cdF) |

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
git clone https://github.com/VEra-Resonance/AEraLogin_Live.git
cd AEraLogin_Live

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
# BASE Mainnet RPC
BASE_RPC_URL=https://mainnet.base.org

# Backend Wallet (Operator - with delegated MINTER_ROLE, UPDATER_ROLE)
# This wallet executes daily operations like NFT minting and score updates
PRIVATE_KEY=your_private_key_here

# Smart Contracts
IDENTITY_NFT_ADDRESS=0xF9ff5DC523927B9632049bd19e17B610E9197d53
RESONANCE_SCORE_ADDRESS=0x9A814DBF7E2352CE9eA6293b4b731B2a24800102
RESONANCE_REGISTRY_ADDRESS=0xAAf30d96382D2409Cf1626095e97BEc1C59e5cdF

# Server
PORT=8840
```

### Wallet Architecture

| Wallet | Address | Purpose |
|--------|---------|---------|
| **Safe Wallet** (Gnosis Safe) | `0xC8B1bEb43361bb78400071129139A37Eb5c5Dd93` | Multisig admin holding DEFAULT_ADMIN_ROLE. Governance & emergency actions. |
| **Backend Wallet** (Operator) | `0x22A2cAcB19e77D25da063A787870a3EE6BAC8Dfe` | Hot wallet with delegated roles. Executes daily operations. |
| **Donation Wallet** | `0x27F8233Ae2FC3945064c0bad72267e68bC28AaAa` | Community donations for gas fee sponsoring. |

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
2. **Connect MetaMask** - Ensure you're on BASE Mainnet network
3. **Sign Authentication** - Verify wallet ownership
4. **Receive Identity NFT** - Automatically minted on first login (gasless!)
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
  "contract_address": "0xF9ff5DC523927B9632049bd19e17B610E9197d53",
  "basescan_url": "https://basescan.org/nft/..."
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
  "network": "BASE Mainnet"
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

- **Backend**: FastAPI, Python 3.13+
- **Blockchain**: Web3.py, eth-account
- **Frontend**: Vanilla JS, Web3.js, MetaMask
- **Database**: SQLite
- **Network**: BASE Mainnet (L2)

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
3. **Verify all contracts on Basescan**
4. **Regular security audits**

---

## 🌟 Why BASE Mainnet?

### Cost Comparison

| Operation | Ethereum Mainnet | BASE Mainnet | Savings |
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

- **Dashboard V2 with cross-platform resonance analytics** - Enhanced user insights
- **Optional Miniapp integration** - Once SIWE is supported natively in Base Miniapps

---

## 📝 License

Apache License 2.0 - See [LICENSE](LICENSE) file for details

---

## 🔗 Links

- **Repository**: https://github.com/VEra-Resonance/AEraLogin_Live
- **BASE Network**: https://base.org
- **BASE Explorer**: https://basescan.org
- **Coinbase L2 Docs**: https://docs.base.org

---

## 🤝 Contributing

This is an open-source project. Contributions are welcome!

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

---

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Review smart contracts on Basescan
- Check BASE network status

---

**Built with ❤️ on BASE Mainnet - Coinbase's Ethereum L2 Solution**
