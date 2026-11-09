# Testing Guide

## Overview

ThreatShield includes comprehensive testing across backend, frontend, and smart contracts.

## Backend Testing

### Setup

```bash
cd backend
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

### Run Specific Tests

```bash
# Test authentication
pytest tests/test_auth.py

# Test analyzers
pytest tests/test_analyzers.py

# Test API endpoints
pytest tests/test_api_analyze.py
```

### Test Cases Covered

#### Authentication Tests
- ✅ User registration
- ✅ Duplicate email/username handling
- ✅ Login with valid credentials
- ✅ Login with invalid credentials
- ✅ JWT token generation
- ✅ Protected endpoint access

#### URL Analyzer Tests
- ✅ Normal URL analysis
- ✅ Suspicious TLD detection
- ✅ Typosquatting detection
- ✅ IP address URL detection
- ✅ Suspicious keyword detection
- ✅ Risk scoring calculation

#### Message Analyzer Tests
- ✅ Benign message analysis
- ✅ Urgency manipulation detection
- ✅ Credential request detection
- ✅ Payment request detection
- ✅ URL extraction
- ✅ Brand impersonation detection

#### API Integration Tests
- ✅ URL analysis endpoint
- ✅ Message analysis endpoint
- ✅ Domain analysis endpoint
- ✅ TLS analysis endpoint
- ✅ Authorization checks

## Smart Contract Testing

### Setup

```bash
cd blockchain
npm install
```

### Compile Contracts

```bash
npx hardhat compile
```

### Run Tests

```bash
npx hardhat test
```

### Test with Gas Reporting

```bash
REPORT_GAS=true npx hardhat test
```

### Coverage

```bash
npx hardhat coverage
```

### Test Cases Covered

#### ThreatIntelRegistry Contract
- ✅ Contract deployment
- ✅ Report registration
- ✅ Duplicate prevention
- ✅ Report verification
- ✅ Query by submitter
- ✅ Query by index
- ✅ Event emission
- ✅ Access control

## Frontend Testing

### Setup

```bash
cd frontend
npm install
```

### Run Tests (when implemented)

```bash
npm test
npm run test:coverage
```

### E2E Testing

```bash
npm run test:e2e
```

## Manual Testing

### Test Scenarios

#### 1. Authentication Flow
```
1. Navigate to /register
2. Create new account
3. Verify redirect to dashboard
4. Logout
5. Login with credentials
6. Verify successful authentication
```

#### 2. URL Scanning
```
Test URLs:
- Safe: https://google.com
- Suspicious TLD: http://test-site.tk
- Typosquatting: http://gooogle.com
- IP Address: http://192.168.1.1

Expected:
- Risk classification
- Threat indicators
- Recommendations
```

#### 3. Message Analysis
```
Test Messages:

Benign:
"Hello, thank you for your inquiry. We'll get back to you soon."

Suspicious:
"URGENT! Your account will be closed. Click here immediately: http://suspicious.com"

Phishing:
"Your PayPal account requires verification. Enter your password and OTP here."

Expected:
- Risk level classification
- Suspicious pattern detection
- Impersonation detection
- Extracted indicators
```

#### 4. TLS Certificate Analysis
```
Test Domains:
- Valid cert: google.com
- Expired cert: expired.badssl.com
- Wrong host: wrong.host.badssl.com

Expected:
- Certificate details
- Expiration status
- Hostname match
- Warnings
```

#### 5. Blockchain Verification
```
1. Complete an investigation
2. Register report on blockchain
3. Copy report hash
4. Verify hash on blockchain
5. Confirm verification result
```

## Integration Testing

### Test Environment Setup

```bash
# Start services
docker-compose up -d

# Wait for services
sleep 10

# Run integration tests
pytest tests/integration/
```

### API Testing with curl

```bash
# Register user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","username":"test","password":"test123456"}'

# Login
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123456"}' \
  | jq -r '.access_token')

# Analyze URL
curl -X POST http://localhost:8000/api/analyze/url \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

## Load Testing

### Using locust

```bash
pip install locust

# Create locustfile.py
locust -f tests/load/locustfile.py --host=http://localhost:8000
```

## Security Testing

### SSRF Protection

Test that private IPs are blocked:
```python
# Should be rejected
test_urls = [
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://192.168.1.1",
    "http://169.254.169.254",  # AWS metadata
]
```

### SQL Injection

Test that inputs are properly sanitized:
```python
malicious_inputs = [
    "'; DROP TABLE users;--",
    "1' OR '1'='1",
    "admin'--",
]
```

### XSS Protection

Test that outputs are escaped:
```html
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
```

## CI/CD Testing

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r backend/requirements.txt
      - run: pytest backend/tests/

  blockchain:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: cd blockchain && npm install
      - run: cd blockchain && npx hardhat test
```

## Test Data

### Sample Threat URLs
- Phishing: http://paypa1.com (note the '1')
- Malware: (use URLhaus test data)
- Suspicious: http://urgent-verify-account.tk

### Sample Messages
- Benign business email
- Password reset phishing
- Prize scam
- Urgent account verification

## Performance Benchmarks

Expected performance:
- URL analysis: < 3 seconds
- Message analysis: < 2 seconds
- TLS analysis: < 5 seconds
- API response: < 200ms (excluding analysis)

## Troubleshooting Tests

### Database Connection Issues
```bash
# Reset test database
dropdb threat_intel_test
createdb threat_intel_test
```

### Port Conflicts
```bash
# Check ports
lsof -i :8000
lsof -i :3000
```

### Clean Test Environment
```bash
# Remove containers
docker-compose down -v

# Remove cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type d -name .pytest_cache -exec rm -r {} +
```
