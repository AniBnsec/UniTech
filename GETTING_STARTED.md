# 🚀 Getting Started with ThreatShield

## Welcome! 

You now have a complete, production-ready cybersecurity threat detection platform. This guide will help you get it running in under 10 minutes.

---

## ⚡ Quick Start (Choose Your Path)

### Option A: Docker (Easiest - 2 Minutes)

```bash
# 1. Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# 2. Start everything
docker-compose up -d

# 3. Open your browser
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
```

That's it! Skip to [First Steps](#first-steps).

---

### Option B: Manual Setup (10 Minutes)

#### Prerequisites Check

```bash
# Check you have everything
node --version   # Should be 18+
python --version # Should be 3.11+
psql --version   # Should be 14+
```

Don't have them? [Install Prerequisites](#install-prerequisites)

#### 1. Database Setup (2 minutes)

```bash
# Create database
createdb threat_intel

# Or using psql
psql -U postgres
CREATE DATABASE threat_intel;
\q
```

#### 2. Backend Setup (3 minutes)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and edit environment
cp .env.example .env
# Edit .env and set: DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/threat_intel

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

Keep this terminal open! Backend is now running at http://localhost:8000

#### 3. Frontend Setup (3 minutes)

Open a NEW terminal:

```bash
cd frontend

# Install dependencies
npm install

# Copy environment
cp .env.example .env.local

# Start development server
npm run dev
```

Frontend is now running at http://localhost:3000

---

## 🎯 First Steps

### 1. Create Your Account

1. Open http://localhost:3000
2. Click **"Get Started"** or **"Sign Up"**
3. Fill in:
   - Username: `yourname`
   - Email: `you@example.com`
   - Password: `SecurePass123`
4. Click **"Create Account"**
5. You'll be redirected to the dashboard!

### 2. Try Your First Scan

#### URL Scanner

1. Click **"URL Scanner"** in the sidebar
2. Paste this URL: `https://google.com`
3. Click **"Scan URL"**
4. Wait 2-3 seconds
5. See the results with risk assessment!

Try a suspicious URL: `http://suspicious-login-verify.tk`

#### Message Scanner

1. Click **"Message Scanner"**
2. Paste this message:
```
URGENT! Your account will be suspended.
Click here to verify: http://verify-account.tk
Enter your password and OTP immediately.
```
3. Click **"Analyze Message"**
4. See the scam detection results!

#### TLS Analyzer

1. Click **"TLS Analyzer"**
2. Enter: `google.com`
3. Click **"Analyze"**
4. View the certificate details!

### 3. Explore the Dashboard

1. Go back to **"Dashboard"**
2. See your investigation statistics
3. View activity charts
4. Browse recent scans

---

## 🎓 Learn the Features

### Understanding Risk Levels

- **🟢 LOW RISK**: No significant threats detected
- **🟡 SUSPICIOUS**: Some concerning indicators found
- **🔴 HIGH RISK**: Multiple threat indicators detected
- **⚫ MALICIOUS**: Confirmed threat by intelligence sources

### Reading Analysis Results

Each analysis shows:
- **Risk Score** (0-100): Higher = more dangerous
- **Confidence**: How sure the system is
- **Indicators**: Specific threats found
- **Evidence**: Why each indicator was flagged
- **Recommendations**: What you should do

---

## 🔧 Configuration (Optional)

### Adding Threat Intelligence APIs

To enhance detection, add API keys to `backend/.env`:

```env
# URLhaus (Free, no key needed - already works!)
URLHAUS_API_URL=https://urlhaus-api.abuse.ch/v1/

# Google Safe Browsing (Free tier available)
GOOGLE_SAFE_BROWSING_API_KEY=your_key_here

# VirusTotal (Free tier: 4 requests/min)
VIRUSTOTAL_API_KEY=your_key_here
```

Get keys:
- Safe Browsing: https://developers.google.com/safe-browsing/v4/get-started
- VirusTotal: https://www.virustotal.com/gui/join-us

Then restart the backend:
```bash
# Stop with Ctrl+C, then:
uvicorn app.main:app --reload
```

---

## 🧪 Testing Your Setup

### Quick Health Check

```bash
# Test backend
curl http://localhost:8000/health

# Should see: {"status":"healthy","version":"1.0.0"}
```

### Run Automated Tests

```bash
# Backend tests
cd backend
pytest

# Smart contract tests
cd blockchain
npm install
npx hardhat test
```

---

## 🚨 Troubleshooting

### Backend won't start?

**Error**: "Connection refused" or database error

```bash
# Check PostgreSQL is running
# Windows:
pg_ctl status

# Mac:
brew services list

# Linux:
sudo systemctl status postgresql

# Start if needed
sudo systemctl start postgresql
```

**Error**: "Port 8000 already in use"

```bash
# Kill the process
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

### Frontend won't start?

**Error**: "Port 3000 already in use"

```bash
# Kill the process  
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:3000 | xargs kill -9
```

**Error**: Module not found

```bash
# Clean install
rm -rf node_modules .next
npm install
npm run dev
```

### Can't create database?

```bash
# Connect as postgres user
sudo -u postgres psql

# Then:
CREATE DATABASE threat_intel;
\q
```

### Still having issues?

1. Check you're in the right directory
2. Verify all environment variables are set
3. Make sure no firewalls are blocking ports
4. Try the Docker option instead
5. Check logs for specific errors

---

## 📚 Next Steps

### Learn More

- **API Documentation**: http://localhost:8000/docs
- **Feature List**: Read `FEATURES.md`
- **Testing Guide**: Read `docs/TESTING.md`
- **Deployment**: Read `docs/DEPLOYMENT.md`

### Customize the Platform

- **Add Analysis Rules**: Edit `backend/app/analyzers/*.py`
- **Modify Risk Scoring**: Update weights in analyzers
- **Customize UI**: Edit `frontend/app/**/*.tsx`
- **Add Threat Intel**: Create new integrations in `backend/app/intelligence/`

### Deploy to Production

Ready to go live? Follow `docs/DEPLOYMENT.md`:

1. Deploy frontend to Vercel
2. Deploy backend to Render
3. Use managed PostgreSQL
4. Deploy smart contract to mainnet (optional)

---

## 🔐 Security Reminders

✅ **DO**:
- Change `JWT_SECRET` before deploying
- Use strong passwords
- Keep API keys secret
- Review security checklist in DEPLOYMENT.md

❌ **DON'T**:
- Commit `.env` files
- Use default secrets in production
- Expose private keys
- Skip security updates

---

## 💡 Pro Tips

### Development Workflow

```bash
# Terminal 1: Backend with auto-reload
cd backend
uvicorn app.main:app --reload

# Terminal 2: Frontend with fast refresh
cd frontend
npm run dev

# Terminal 3: Run tests
cd backend
pytest --watch
```

### Useful Commands

```bash
# View API docs
open http://localhost:8000/docs

# Check database
psql threat_intel

# View logs
docker-compose logs -f

# Reset database
alembic downgrade base
alembic upgrade head
```

### Sample Test Data

Use these for testing:

**Safe URLs**:
- https://google.com
- https://github.com
- https://microsoft.com

**Suspicious URLs** (for testing detection):
- http://gooogle.com (typosquatting test)
- http://urgent-verify-account.tk (suspicious pattern)
- http://192.168.1.1 (IP address test)

**Scam Messages**:
```
URGENT! Your account will be closed immediately!
Click here to verify: http://verify-now.xyz
Enter your password and OTP code to continue.
```

---

## 🎉 You're Ready!

Congratulations! You now have a fully functional cybersecurity platform.

### What You Can Do Now:

✅ Scan URLs for threats
✅ Analyze suspicious messages
✅ Check TLS certificates
✅ View threat intelligence
✅ Monitor your dashboard
✅ Review investigation history

### Share Your Work:

- Demo it to friends
- Present at a hackathon
- Add to your portfolio
- Deploy to production
- Contribute improvements

---

## 📞 Need Help?

- 📖 Read the docs in `/docs`
- 🐛 Check error messages carefully
- 🔍 Search issues in code
- 💬 Review inline comments
- 🧪 Run tests to verify setup

---

## 🌟 Make It Yours

This is YOUR platform now. Feel free to:

- Add new analysis features
- Integrate more threat intel sources
- Customize the UI design
- Add machine learning models
- Create mobile apps
- Build browser extensions
- Share with the community

---

**Happy Threat Hunting! 🛡️**

*Remember: This tool is for education and research. Always verify findings through multiple sources!*
