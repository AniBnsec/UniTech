# AI-Powered Web Threat Detection & Digital Trust Intelligence

A comprehensive cybersecurity platform that combines AI, threat intelligence, and blockchain technology to investigate suspicious websites, phishing URLs, fraudulent messages, and security vulnerabilities.

## 🎯 Core Features

- **AI-Powered URL Analysis**: Detect phishing, typosquatting, and malicious domains
- **TLS Certificate Validator**: Comprehensive certificate chain and trust analysis
- **Scam Message Detection**: AI-powered analysis of suspicious emails and messages
- **Website Security Assessment**: Non-intrusive security header and configuration checks
- **Threat Correlation Engine**: Identify relationships between security incidents
- **Blockchain Verification**: Tamper-evident threat report registry on EVM testnets
- **Real-time Threat Intelligence**: Integration with URLhaus, Safe Browsing, and more

## 🏗️ Technology Stack

### Frontend
- Next.js 14 with App Router
- React 18 + TypeScript
- Tailwind CSS + shadcn/ui
- Framer Motion for animations
- Recharts for data visualization
- ethers.js for Web3 integration

### Backend
- FastAPI (Python)
- PostgreSQL + SQLAlchemy
- Redis for caching
- HTTPX for async HTTP requests
- Pydantic for data validation

### Blockchain
- Solidity smart contracts
- Hardhat development environment
- EVM-compatible testnet deployment
- MetaMask integration

### Security & AI
- OpenAI/Anthropic LLM integration
- Certificate Transparency logs
- URLhaus, Safe Browsing APIs
- Custom threat detection algorithms

## 📦 Project Structure

```
web-threat-intelligence/
├── frontend/              # Next.js application
│   ├── app/              # App router pages
│   ├── components/       # Reusable UI components
│   ├── features/         # Feature-specific components
│   ├── services/         # API service layer
│   └── types/            # TypeScript definitions
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── analyzers/   # Threat analysis engines
│   │   ├── intelligence/# Threat intel integrations
│   │   └── services/    # Business logic
│   └── tests/           # Backend tests
├── blockchain/          # Smart contracts
│   ├── contracts/       # Solidity contracts
│   ├── scripts/         # Deployment scripts
│   └── test/            # Contract tests
└── docs/                # Documentation
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- PostgreSQL 14+
- Redis (optional, for caching)
- MetaMask wallet (for blockchain features)

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
# Configure your environment variables
npm run dev
```

Frontend will be available at `http://localhost:3000`

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Configure your environment variables
alembic upgrade head
uvicorn app.main:app --reload
```

Backend API will be available at `http://localhost:8000`

### Blockchain Setup

```bash
cd blockchain
npm install
cp .env.example .env
# Configure your testnet RPC and private key
npx hardhat compile
npx hardhat test
npx hardhat run scripts/deploy.ts --network sepolia
```

## 🔧 Environment Configuration

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CONTRACT_ADDRESS=
NEXT_PUBLIC_CHAIN_ID=11155111
```

### Backend (.env)

```env
DATABASE_URL=postgresql://user:password@localhost:5432/threat_intel
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# AI/LLM Configuration
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# Threat Intelligence APIs
URLHAUS_API_URL=https://urlhaus-api.abuse.ch/v1/
GOOGLE_SAFE_BROWSING_API_KEY=
VIRUSTOTAL_API_KEY=
PHISHTANK_API_KEY=

# Blockchain
BLOCKCHAIN_RPC_URL=
PRIVATE_KEY=
CONTRACT_ADDRESS=
ETHERSCAN_API_KEY=
```

## 📊 Database Setup

```bash
cd backend
# Create database
createdb threat_intel

# Run migrations
alembic upgrade head

# (Optional) Seed test data
python -m app.database.seed
```

## 🧪 Testing

### Frontend Tests
```bash
cd frontend
npm run test
npm run test:e2e
```

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app tests/
```

### Smart Contract Tests
```bash
cd blockchain
npx hardhat test
npx hardhat coverage
```

## 🔐 Security Features

- **SSRF Protection**: Validates URLs and blocks private IP ranges
- **Rate Limiting**: Prevents abuse of analysis endpoints
- **Input Validation**: All inputs sanitized on backend
- **JWT Authentication**: Secure session management
- **Role-Based Access Control**: User, Analyst, Admin roles
- **Audit Logging**: All security-relevant events recorded
- **Privacy-First**: Sensitive data never stored on-chain

## 🎨 Design System

The platform uses a premium dark-first design with:
- Professional navy/charcoal backgrounds
- Electric blue and cyan accents
- Clean typography and spacing
- Glass-effect panels for depth
- Smooth micro-interactions
- Fully responsive layouts

## 📖 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🚢 Deployment

### Frontend (Vercel)
```bash
cd frontend
vercel deploy
```

### Backend (Render/Railway)
- Connect your GitHub repository
- Set environment variables
- Deploy from main branch

### Database (Managed PostgreSQL)
- Use Supabase, Railway, or Render PostgreSQL
- Run migrations after deployment

## 🤝 Contributing

This project is designed for educational and research purposes. Contributions are welcome!

## 📄 License

MIT License - See LICENSE file for details

## ⚠️ Disclaimer

This platform is for educational and research purposes. Always:
- Use authorized testing environments only
- Respect API rate limits and terms of service
- Never perform unauthorized security testing
- Understand that LOW RISK ≠ guaranteed safe
- Verify findings through multiple sources

## 🆘 Support

For issues, questions, or suggestions:
- Open a GitHub issue
- Check the documentation in `/docs`
- Review API documentation at `/docs` endpoint

---

**Built with ❤️ for cybersecurity education and threat intelligence**
