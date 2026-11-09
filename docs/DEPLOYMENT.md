# Deployment Guide

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL 14+
- Redis (optional, for caching)
- MetaMask wallet (for blockchain features)

## Backend Deployment

### 1. Environment Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/threat_intel
JWT_SECRET=your-super-secret-key-here
OPENAI_API_KEY=your-openai-key  # Optional
ANTHROPIC_API_KEY=your-anthropic-key  # Optional
GOOGLE_SAFE_BROWSING_API_KEY=your-key  # Optional
```

### 3. Database Setup

```bash
# Create database
createdb threat_intel

# Run migrations
alembic upgrade head
```

### 4. Run Backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Deploy to Render

1. Connect your GitHub repository
2. Create new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Create PostgreSQL database add-on

## Frontend Deployment

### 1. Environment Setup

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
NEXT_PUBLIC_CONTRACT_ADDRESS=0x...
NEXT_PUBLIC_CHAIN_ID=11155111
```

### 3. Build and Test

```bash
npm run build
npm start
```

### Deploy to Vercel

```bash
npm install -g vercel
vercel login
vercel deploy --prod
```

Or connect GitHub repository to Vercel dashboard.

## Blockchain Deployment

### 1. Setup

```bash
cd blockchain
npm install
```

### 2. Configure Network

Create `.env`:

```env
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/YOUR_KEY
PRIVATE_KEY=your_private_key_without_0x
ETHERSCAN_API_KEY=your_etherscan_key
```

### 3. Compile and Test

```bash
npx hardhat compile
npx hardhat test
```

### 4. Deploy to Sepolia Testnet

```bash
npx hardhat run scripts/deploy.ts --network sepolia
```

Copy the contract address to your environment variables.

### 5. Verify on Etherscan

```bash
npx hardhat verify --network sepolia <CONTRACT_ADDRESS>
```

## Post-Deployment

1. Test authentication flow
2. Run URL analysis with known safe/malicious URLs
3. Test TLS certificate analysis
4. Verify blockchain registration
5. Monitor logs for errors
6. Set up monitoring (Sentry, LogRocket, etc.)

## Troubleshooting

### Database Connection Issues
- Check DATABASE_URL format
- Ensure PostgreSQL is running
- Verify network access

### API Connection Issues
- Check CORS settings in backend
- Verify API_URL in frontend
- Check SSL certificate

### Blockchain Issues
- Ensure sufficient testnet ETH
- Verify RPC URL is accessible
- Check network ID matches

## Production Checklist

- [ ] Change all default secrets
- [ ] Enable rate limiting
- [ ] Configure HTTPS
- [ ] Set up database backups
- [ ] Enable monitoring
- [ ] Configure error tracking
- [ ] Set up CI/CD pipeline
- [ ] Review security headers
- [ ] Test disaster recovery
- [ ] Document runbook procedures
