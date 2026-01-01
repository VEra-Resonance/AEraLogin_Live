# AEra Identity & Resonance System

**AEra LogIn — Human-verified identity and on-chain resonance scoring on Coinbase's BASE L2.**

A Web3 authentication and reputation system built on Coinbase's BASE Layer 2 network, featuring dual NFT systems (Identity + Profile), tiered Resonance Scores, and multi-platform follower tracking with OpenSea integration.

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
- **RPC URL**: https://base-rpc.publicnode.com
- **Block Explorer**: https://basescan.org
- **Event API**: https://base.blockscout.com/api/v2

---

## 🎯 Features

### Dual NFT System
- ✅ **Identity NFTs** - Soulbound ERC-721 authentication tokens (automatic on signup)
- ✅ **Profile NFTs** - Optional ERC-721 display layer with OpenSea integration (user-initiated)
- ✅ **Privacy Controls** - Profile NFTs support PUBLIC/PRIVATE visibility toggle
- ✅ **Delegate Pattern** - Gasless visibility changes via backend delegation
- ✅ **Dynamic Metadata** - Real-time on-chain data reflected in NFT attributes

### Reputation System (Tiered Scoring Model)
- ✅ **Resonance Score** - On-chain reputation tracking (50-200 scale)
- ✅ **Tiered Scoring** - Progressive difficulty system:
  - 50-60: +1.0 points per interaction
  - 60-70: +0.5 points per interaction
  - 70-80: +0.2 points per interaction
  - 80-90: +0.1 points per interaction
  - 90-100: +0.01 points per interaction
- ✅ **Dual Score System** - Base Score (50-100) + Owner Score (0-100)
  - **Base Score**: Individual activities and logins
  - **Owner Score**: Average of followers' scores
  - **Total Resonance**: Base + Owner (50-200 range)
- ✅ **6-Tier Ranking**:
  - No Tier (< 51): Below minimum threshold
  - Common (51-100): Base level
  - Uncommon (101-130): Growing influence
  - Rare (131-160): Strong community
  - Epic (161-180): Major influence
  - Legendary (181-200): Maximum resonance

**Tier Visual Guide:**

```
┌──────────────────────────────────────────────────────────────┐
│  🏆 TIER SYSTEM - Resonance Score (50-200)                   │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  🟡 LEGENDARY  (181-200)  ████████████████████  Gold/Orange  │
│     Maximum Resonance - Elite Status                         │
│                                                               │
│  🟣 EPIC       (161-180)  ██████████████████    Purple/Blue  │
│     Major Influence - Community Leader                       │
│                                                               │
│  🔵 RARE       (131-160)  ████████████████      Blue/Cyan    │
│     Strong Community - Rising Star                           │
│                                                               │
│  🟢 UNCOMMON   (101-130)  ██████████████        Green        │
│     Growing Influence - Active Contributor                   │
│                                                               │
│  ⚪ COMMON     (51-100)   ██████████            Gray/Blue    │
│     Base Level - Starting Journey                            │
│                                                               │
│  ⚫ NO TIER    (< 51)     ██                    Dark Gray    │
│     Below Threshold - Need More Activity                     │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```
- ✅ **Blockchain Sync** - Real-time score updates with float precision (rounded on-chain)

### Tiered Scoring Details

**Score Progression Table:**

| Score Range | Points/Interaction | Interactions for +10 | Total to Reach |
|-------------|-------------------|---------------------|----------------|
| 50-60 | +1.0 | 10 | Start (50) |
| 60-70 | +0.5 | 20 | 60 |
| 70-80 | +0.2 | 50 | 80 |
| 80-90 | +0.1 | 100 | 130 |
| 90-100 | +0.01 | 1000 | 230 |

**Total Interactions Needed:**
- 50 → 60: 10 interactions
- 60 → 70: 20 interactions
- 70 → 80: 50 interactions
- 80 → 90: 100 interactions
- 90 → 100: 1000 interactions
- **Total 50 → 100**: **1180 interactions** (vs. 50 in old system)

**Owner Score Bonus:**
- Followers contribute to your Owner Score
- Owner Score = Average of your followers' base scores
- Range: 0-100 points
- Total Resonance = Base (50-100) + Owner (0-100) = 50-200

### OpenSea Integration
- ✅ **Dynamic NFT Images** - SVG generation with tier-based colors
- ✅ **Rich Metadata** - Token ID, Tier, Resonance Score, Owner Score, Followers, Logins
- ✅ **Privacy-Aware** - Private NFTs show placeholder image/metadata
- ✅ **Live Collection** - View on [OpenSea](https://opensea.io/collection/aera-profile)

### Social Features
- ✅ **Multi-Platform Tracking** - Twitter, Discord, Telegram, Direct links
- ✅ **Follower Dashboard** - Track verified followers and their scores
- ✅ **On-Chain Interactions** - All interactions recorded via recordInteraction()
  - FOLLOW interactions with weight=1 (contract validation compliant)
  - InteractionRecorded events emitted on blockchain
  - Complete interaction history queryable via Blockscout API
- ✅ **Blockchain History Display** - Real-time interaction timeline with icons (👥📤💬🤝🏆)
- ✅ **Platform Integration** - Easy embedding with referral links

---

## 🏗️ Architecture

### Smart Contracts (BASE Mainnet)

| Contract | Address | Purpose | Explorer |
|---------|---------|---------|----------|
| **AEraIdentityNFT** | `0xF9ff5DC523927B9632049bd19e17B610E9197d53` | Soulbound Identity NFT (automatic) | [View on Basescan](https://basescan.org/address/0xF9ff5DC523927B9632049bd19e17B610E9197d53) |
| **AEraProfileNFT** | `0x0a630A3Dc0C7387e0226D1b285C43B753506b27E` | Optional Profile NFT (OpenSea display) | [View on Basescan](https://basescan.org/address/0x0a630A3Dc0C7387e0226D1b285C43B753506b27E) |
| **AEraResonanceScore** | `0x9A814DBF7E2352CE9eA6293b4b731B2a24800102` | On-chain reputation score (ERC-20 standard) | [View on Basescan](https://basescan.org/address/0x9A814DBF7E2352CE9eA6293b4b731B2a24800102) |
| **AEraResonanceRegistry** | `0xAAf30d96382D2409Cf1626095e97BEc1C59e5cdF` | Interaction & follower log | [View on Basescan](https://basescan.org/address/0xAAf30d96382D2409Cf1626095e97BEc1C59e5cdF) |

### OpenSea Collections

| Collection | Link | Description |
|------------|------|-------------|
| **AEra Profile** | [View Collection](https://opensea.io/collection/aera-profile) | Public display NFTs with dynamic metadata |
| **AEra Identity** | [View Collection](https://opensea.io/collection/aera-identity) | Soulbound authentication tokens |

### Backend Components

- **FastAPI Server** (`server.py`) - REST API, dashboard backend & tiered scoring system (6800+ lines)
- **Web3 Service** (`web3_service.py`) - Full blockchain integration with all 4 smart contracts (1200+ lines)
  - Identity NFT minting & queries
  - Profile NFT management (mint, burn, visibility, delegate)
  - Resonance Score updates with float precision
  - Interaction recording & history via Blockscout API
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
# ===== BLOCKCHAIN INTEGRATION (BASE L2) =====
# BASE Mainnet Network (PublicNode - reliable)
BASE_SEPOLIA_RPC_URL=https://base-rpc.publicnode.com
BASE_NETWORK_CHAIN_ID=8453

# BASE Mainnet Blockscout API for Event Queries (no API key needed!)
BLOCKSCOUT_API_URL=https://base.blockscout.com/api/v2

# Contract Addresses (BASE Mainnet)
IDENTITY_NFT_ADDRESS=0xF9ff5DC523927B9632049bd19e17B610E9197d53
RESONANCE_SCORE_ADDRESS=0x9A814DBF7E2352CE9eA6293b4b731B2a24800102
REGISTRY_ADDRESS=0xAAf30d96382D2409Cf1626095e97BEc1C59e5cdF

# AEra Profile NFT (OPTIONAL - Public Display Layer)
PROFILE_NFT_ADDRESS=0x0a630A3Dc0C7387e0226D1b285C43B753506b27E

# Backend Wallet (SYSTEM_ROLE for Registry)
BACKEND_PRIVATE_KEY=your_private_key_here
BACKEND_ADDRESS=0x22A2cAcB19e77D25DA063A787870A3eE6BAC8Dfe

# Server
HOST=0.0.0.0
PORT=8840
PUBLIC_URL=https://aeralogin.com
```

### Wallet Architecture

| Wallet | Address | Purpose |
|--------|---------|---------|
| **Safe Wallet** (Gnosis Safe) | `0xC8B1bEb43361bb78400071129139A37Eb5c5Dd93` | Multisig admin holding DEFAULT_ADMIN_ROLE. Governance & emergency actions. |
| **Backend Wallet** (Operator) | `0x22A2cAcB19e77D25DA063A787870A3eE6BAC8Dfe` | Hot wallet with MINTER_ROLE, ADMIN_ROLE, SYSTEM_ROLE. Executes daily operations & gasless delegation. |
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

1. **Visit Landing Page**: `https://aeralogin.com`
2. **Connect MetaMask** - Ensure you're on BASE Mainnet network
3. **Sign Authentication** - Verify wallet ownership (EIP-4361)
4. **Receive Identity NFT** - Automatically minted on first login (gasless!)
5. **Access Dashboard** - View your followers and Resonance Score
6. **Mint Profile NFT** (Optional) - Create public display NFT for OpenSea
7. **Toggle Visibility** - Set Profile NFT PUBLIC/PRIVATE
8. **Delegate Backend** (Optional) - Enable gasless visibility changes

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

**Profile NFT:**
```bash
# Check Profile NFT status
GET /api/profile-nft/status/{address}

# Mint Profile NFT (user-initiated only)
POST /api/profile-nft/mint
{
  "wallet_signature": "0x...",
  "message": "...",
  "address": "0x..."
}

# Toggle visibility
POST /api/profile-nft/visibility
{
  "token_id": 1,
  "is_public": true,
  "wallet_signature": "0x..."
}

# Get public metadata (OpenSea)
GET /api/profile/public/{token_id}

# Get dynamic image (OpenSea)
GET /api/profile/image/{token_id}

# Burn Profile NFT
POST /api/profile-nft/burn
{
  "wallet_signature": "0x..."
}
```

**Resonance Score:**
```bash
# Get score
GET /api/blockchain/score/{address}

# Returns:
{
  "db_score": 81.5,
  "blockchain_score": 130.0,
  "owner_score": 48.5,
  "tier": "Uncommon",
  "last_synced": "2025-12-31T10:30:00Z"
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
├── server.py                 # FastAPI backend (6800+ lines)
│                             # - Tiered scoring system
│                             # - Profile NFT management
│                             # - OpenSea metadata endpoints
├── web3_service.py          # Blockchain integration (1200+ lines)
│                             # - 4 contract integrations
│                             # - Profile NFT functions
│                             # - Delegate pattern support
│                             # - Blockscout API queries
├── airdrop_worker.py        # Background task processor
├── logger.py                # Centralized logging system
├── index.html               # Landing page
├── user-dashboard.html      # User dashboard with Profile NFT controls
├── blockchain-dashboard.js  # Frontend blockchain interactions
├── set_profile_base_uris.py # Contract configuration script
├── requirements.txt         # Python dependencies
├── .env                     # Environment configuration (gitignored)
├── .gitignore              # Security protection (extended)
└── backups/                 # Local backups (not in git)
```

### Technology Stack

- **Backend**: FastAPI, Python 3.13+
- **Blockchain**: Web3.py 7.x, eth-account
- **Frontend**: Vanilla JS, Web3.js, MetaMask
- **Database**: SQLite (Float support for tiered scoring)
- **Network**: BASE Mainnet (Chain ID 8453)
- **APIs**: Blockscout v2 API for event queries
- **NFT Standards**: ERC-721 (Identity & Profile NFTs), ERC-20 (Resonance Score)

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
| Identity NFT Mint | ~$1.00 | ~$0.0003 | 99.97% |
| Profile NFT Mint | ~$1.00 | ~$0.0003 | 99.97% |
| Score Update | ~$0.50 | ~$0.0002 | 99.96% |
| Registry Entry | ~$0.75 | ~$0.0002 | 99.97% |
| Visibility Toggle | ~$0.30 | ~$0.0001 | 99.97% |

### Technical Benefits

- **Ethereum Compatibility** - All Solidity contracts work without changes
- **Fast Finality** - Transactions confirm in seconds
- **Low Fees** - Enable micro-transactions and frequent updates
- **Coinbase Support** - Backed by major crypto exchange
- **Growing Ecosystem** - Active developer community
- **Blockscout API** - Free event queries without API keys

---

## 🎨 Profile NFT Features

### Dynamic Metadata
- **Real-time Updates** - Reflects current Resonance Score and stats
- **Tier-Based Colors** - Visual representation of user ranking
- **Privacy Controls** - PUBLIC/PRIVATE toggle with custom placeholders

### OpenSea Display
```json
{
  "name": "AEra Profile #1",
  "description": "Verified human identity with Resonance Score 130",
  "image": "https://aeralogin.com/api/profile/image/1",
  "attributes": [
    {"trait_type": "Token ID", "value": 1},
    {"trait_type": "Tier", "value": "Uncommon"},
    {"trait_type": "Resonance Score", "value": 130.0},
    {"trait_type": "Owner Score", "value": 49.0},
    {"trait_type": "Followers", "value": 19},
    {"trait_type": "Logins", "value": 68}
  ]
}
```

### Delegate Pattern
**Problem**: Visibility changes cost gas (~$0.001 per toggle)

**Solution**: One-time delegation to backend wallet
1. User delegates once (pays ~$0.001)
2. Backend can then toggle visibility for free
3. User retains full NFT ownership

**Contract Function**: `setDelegate(uint256 tokenId, address delegate)`

---

## 🛣️ Roadmap

### Completed ✅
- **Dual NFT System** - Identity + Profile NFTs deployed
- **Tiered Scoring** - Progressive difficulty (1180 interactions for 50→100)
- **OpenSea Integration** - Dynamic metadata & SVG images
- **Delegate Pattern** - Gasless visibility changes
- **6-Tier Ranking** - Score range 50-200 with color-coded tiers
- **Blockscout API** - Event queries without API keys

### In Progress 🚧
- **Cross-Platform Analytics** - Enhanced resonance tracking
- **Mobile Optimization** - Better UX for mobile wallets

### Future Plans 🔮
- **NFT Utilities** - Profile NFT holder benefits
- **Social Graphs** - Follower network visualization
- **Miniapp Integration** - Once SIWE is supported natively in Base Miniapps
- **Token Gating** - Access control based on Resonance Score tiers

---

## 📊 Key Metrics

### Live Statistics
- **Network**: BASE Mainnet (Chain ID 8453)
- **Total Users**: Query via `/api/stats`
- **Identity NFTs Minted**: Check contract on Basescan
- **Profile NFTs Minted**: Check contract on Basescan
- **Average Gas Cost**: ~$0.0002 per transaction
- **Blockchain Sync Status**: Real-time via dashboard

### Contract Verification
All contracts are verified on Basescan:
- Identity NFT: [0xF9ff...7d53](https://basescan.org/address/0xF9ff5DC523927B9632049bd19e17B610E9197d53)
- Profile NFT: [0x0a63...b27E](https://basescan.org/address/0x0a630A3Dc0C7387e0226D1b285C43B753506b27E)
- Resonance Score: [0x9A81...0102](https://basescan.org/address/0x9A814DBF7E2352CE9eA6293b4b731B2a24800102)
- Registry: [0xAAf3...5cdF](https://basescan.org/address/0xAAf30d96382D2409Cf1626095e97BEc1C59e5cdF)

---

## 📝 License

Apache License 2.0 - See [LICENSE](LICENSE) file for details

---

## 🔗 Links

### Live Application
- **Website**: https://aeralogin.com
- **User Dashboard**: https://aeralogin.com/dashboard

### Smart Contracts (Basescan)
- **Identity NFT**: https://basescan.org/address/0xF9ff5DC523927B9632049bd19e17B610E9197d53
- **Profile NFT**: https://basescan.org/address/0x0a630A3Dc0C7387e0226D1b285C43B753506b27E
- **Resonance Score**: https://basescan.org/address/0x9A814DBF7E2352CE9eA6293b4b731B2a24800102
- **Registry**: https://basescan.org/address/0xAAf30d96382D2409Cf1626095e97BEc1C59e5cdF

### OpenSea Collections
- **AEra Profile**: https://opensea.io/collection/aera-profile
- **AEra Identity**: https://opensea.io/collection/aera-identity

### Network & Tools
- **BASE Network**: https://base.org
- **BASE Explorer**: https://basescan.org
- **Blockscout API**: https://base.blockscout.com/api/v2
- **Coinbase L2 Docs**: https://docs.base.org

### Repository
- **GitHub**: https://github.com/VEra-Resonance/AEraLogin_Live
- **Issues**: https://github.com/VEra-Resonance/AEraLogin_Live/issues

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
- 📧 **Email**: support@aeralogin.com
- 🐛 **GitHub Issues**: [Report bugs or request features](https://github.com/VEra-Resonance/AEraLogin_Live/issues)
- 💬 **Discord**: Join our community (coming soon)
- 📊 **Contract Status**: Review smart contracts on Basescan
- 🌐 **Network Status**: Check [BASE network status](https://status.base.org)

### Quick Troubleshooting

**MetaMask not connecting?**
- Ensure you're on BASE Mainnet (Chain ID 8453)
- Add network manually: RPC `https://base-rpc.publicnode.com`

**Profile NFT not showing on OpenSea?**
- Wait 1-24 hours for metadata cache refresh
- Click "Refresh metadata" button on OpenSea
- Verify visibility is set to PUBLIC

**Score not updating?**
- Blockchain sync happens after score changes
- Check `/api/blockchain/score/{address}` for sync status
- Float scores are rounded when synced on-chain

---

**Built with ❤️ on BASE Mainnet - Coinbase's Ethereum L2 Solution**

*Last Updated: December 31, 2025*
