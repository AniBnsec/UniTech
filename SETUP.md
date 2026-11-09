# ThreatShield - Quick Setup Guide

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL 14+
- Git

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd UniTech

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
cp blockchain/.env.example blockchain/.env
```

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb threat_intel

# Or using psql
psql -U postgres
CREATE DATABASE threat_intel;
\q
```

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Update .env with your database URL
# DATABASE_URL=postgresql://postgres:password@localhost:5432/threat_intel

# Run migrations
alembic upgrade head

# Start backend server
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

### 4. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

### 5. Test the Application

1. Open browser to `http://localhost:3000`
2. Click "Get Started" or "Sign Up"
3. Create an account
4. You'll be redirected to the dashboard
5. Try the URL Scanner with: `https://google.com`

## 🐳 Docker Setup (Alternative)

If you prefer Docker:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## ⛓️ Blockchain Setup (Optional)

### 1. Install Dependencies

```bash
cd blockchain
npm install
```

### 2. Configure Network

Edit `blockchain/.env`:

```env
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/YOUR_INFURA_KEY
PRIVATE_KEY=your_test_wallet_private_key
ETHERSCAN_API_KEY=your_etherscan_key
```

### 3. Get Test ETH

1. Create MetaMask wallet on Sepolia testnet
2. Get free test ETH from: https://sepoliafaucet.com/

### 4. Compile and Deploy

```bash
# Compile contracts
npx hardhat compile

# Run tests
npx hardhat test

# Deploy to Sepolia testnet
npx hardhat run scripts/deploy.ts --network sepolia

# Copy the contract address to backend/.env and frontend/.env.local
```

## 🧪 Running Tests

### Backend Tests

```bash
cd backend
pytest
pytest --cov=app --cov-report=html
```

### Smart Contract Tests

```bash
cd blockchain
npx hardhat test
npx hardhat coverage
```

## 📝 Configuration

### Backend Environment Variables (.env)

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/threat_intel

# JWT Secret (change in production!)
JWT_SECRET=your-super-secret-key-here

# Optional: AI/LLM APIs
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Threat Intelligence APIs
GOOGLE_SAFE_BROWSING_API_KEY=...
VIRUSTOTAL_API_KEY=...

# Optional: Blockchain
BLOCKCHAIN_RPC_URL=https://sepolia.infura.io/v3/...
CONTRACT_ADDRESS=0x...
```

### Frontend Environment Variables (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CONTRACT_ADDRESS=0x...
NEXT_PUBLIC_CHAIN_ID=11155111
```

## 🎯 Feature Testing Checklist

### Authentication
- [ ] Register new user
- [ ] Login with credentials
- [ ] Access protected pages
- [ ] Logout

### URL Scanner
- [ ] Scan safe URL (google.com)
- [ ] Scan suspicious URL
- [ ] View risk assessment
- [ ] See threat indicators

### Message Scanner
- [ ] Analyze benign message
- [ ] Analyze phishing message
- [ ] View suspicious patterns
- [ ] See recommendations

### TLS Analyzer
- [ ] Analyze valid certificate
- [ ] View certificate details
- [ ] Check expiration
- [ ] See warnings

### Dashboard
- [ ] View statistics
- [ ] See activity charts
- [ ] Browse recent investigations
- [ ] Navigate to history

### Blockchain (Optional)
- [ ] Register report hash
- [ ] Verify report hash
- [ ] View transaction details

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check Python version
python --version  # Should be 3.11+

# Check database connection
psql -U postgres -d threat_intel

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Frontend won't start

```bash
# Clear cache and reinstall
rm -rf node_modules .next
npm install
npm run dev
```

### Database connection error

```bash
# Check PostgreSQL is running
# Windows:
pg_ctl status

# macOS:
brew services list

# Linux:
sudo systemctl status postgresql

# Test connection
psql -U postgres -h localhost
```

### Port already in use

```bash
# Windows - Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

## 📚 Next Steps

1. **Configure API Keys**: Add threat intelligence API keys for enhanced detection
2. **Deploy**: Follow [DEPLOYMENT.md](docs/DEPLOYMENT.md) for production deployment
3. **Customize**: Modify analyzers and risk scoring in `backend/app/analyzers/`
4. **Extend**: Add new features using the modular architecture

## 🆘 Getting Help

- **Documentation**: Check `/docs` folder for detailed guides
- **API Docs**: Visit `http://localhost:8000/docs` when backend is running
- **Issues**: Check console logs for error messages
- **Database**: Use pgAdmin or TablePlus to inspect database

## 🎓 Test Credentials

For development testing:

```
Email: test@example.com
Username: testuser
Password: testpass123
```

(Only works if you create this user via registration)

## ⚡ Performance Tips

1. **Redis Cache**: Install Redis for improved performance
2. **API Keys**: Configure threat intelligence APIs for better detection
3. **Database**: Use connection pooling in production
4. **CDN**: Use CDN for frontend static assets in production

## 🔒 Security Notes

- ⚠️ Change `JWT_SECRET` before deploying to production
- ⚠️ Never commit `.env` files to version control
- ⚠️ Use environment-specific configurations
- ⚠️ Enable HTTPS in production
- ⚠️ Use dedicated test wallet for blockchain features
- ⚠️ Review security checklist in [DEPLOYMENT.md](docs/DEPLOYMENT.md)

## 📦 Project Structure

```
UniTech/
├── frontend/          # Next.js React application
├── backend/           # FastAPI Python backend
├── blockchain/        # Solidity smart contracts
├── docs/             # Documentation
├── docker-compose.yml # Docker configuration
└── README.md         # Project overview
```

## ✅ Verification

Everything working? You should be able to:

1. ✅ Register and login
2. ✅ Scan a URL and see results
3. ✅ Analyze a message
4. ✅ View dashboard statistics
5. ✅ Access investigation history

---

**Built with ❤️ for cybersecurity education and research**

Need help? Check the [API Documentation](docs/API.md), [Deployment Guide](docs/DEPLOYMENT.md), or [Testing Guide](docs/TESTING.md).
