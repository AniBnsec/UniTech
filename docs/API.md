# API Documentation

## Base URL

```
Production: https://api.threatshield.com
Development: http://localhost:8000
```

## Authentication

All protected endpoints require JWT Bearer token:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123"
}

Response: 201 Created
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhb...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "username": "johndoe",
    "role": "user",
    "verified": false,
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}

Response: 200 OK
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhb...",
  "token_type": "bearer",
  "user": { ... }
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <token>

Response: 200 OK
{
  "id": "uuid",
  "email": "user@example.com",
  "username": "johndoe",
  "role": "user",
  "verified": false,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Analysis

#### Analyze URL
```http
POST /api/analyze/url
Authorization: Bearer <token>
Content-Type: application/json

{
  "url": "https://suspicious-site.com",
  "deep_scan": false
}

Response: 200 OK
{
  "id": "uuid",
  "type": "url",
  "target": "https://suspicious-site.com",
  "risk_level": "SUSPICIOUS",
  "risk_score": 45.0,
  "confidence": 0.85,
  "status": "completed",
  "result": {
    "normalized_url": "https://suspicious-site.com",
    "domain_info": { ... },
    "indicators": [ ... ],
    "ai_summary": "...",
    "recommendations": [ ... ]
  },
  "indicators": [ ... ],
  "intelligence_matches": [ ... ],
  "created_at": "2024-01-01T00:00:00Z",
  "completed_at": "2024-01-01T00:00:05Z"
}
```

#### Analyze Message
```http
POST /api/analyze/message
Authorization: Bearer <token>
Content-Type: application/json

{
  "message_text": "Urgent! Verify your account...",
  "message_type": "email",
  "sender": "noreply@suspicious.com"
}

Response: 200 OK
{
  "id": "uuid",
  "type": "message",
  "risk_level": "HIGH_RISK",
  "risk_score": 75.0,
  "result": {
    "suspicious_patterns": [ ... ],
    "extracted_indicators": [ ... ],
    "impersonation_detected": true,
    "ai_analysis": "...",
    "recommendations": [ ... ]
  }
}
```

#### Analyze TLS Certificate
```http
POST /api/analyze/tls
Authorization: Bearer <token>
Content-Type: application/json

{
  "hostname": "example.com"
}

Response: 200 OK
{
  "id": "uuid",
  "type": "tls",
  "risk_level": "LOW_RISK",
  "result": {
    "hostname": "example.com",
    "https_available": true,
    "certificate": {
      "subject": "example.com",
      "issuer": "Let's Encrypt",
      "valid_from": "2024-01-01T00:00:00Z",
      "valid_until": "2024-04-01T00:00:00Z"
    },
    "hostname_match": true,
    "expired": false,
    "days_until_expiry": 90,
    "warnings": []
  }
}
```

### Investigations

#### Get Investigations
```http
GET /api/investigations?page=1&page_size=20
Authorization: Bearer <token>

Response: 200 OK
{
  "items": [ ... ],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "pages": 5
}
```

#### Get Investigation by ID
```http
GET /api/investigations/{investigation_id}
Authorization: Bearer <token>

Response: 200 OK
{ ... investigation object ... }
```

### Dashboard

#### Get Statistics
```http
GET /api/dashboard/stats
Authorization: Bearer <token>

Response: 200 OK
{
  "total_investigations": 150,
  "low_risk_count": 100,
  "suspicious_count": 30,
  "high_risk_count": 15,
  "malicious_count": 5,
  "recent_investigations": [ ... ],
  "threat_categories": [ ... ],
  "daily_activity": [ ... ]
}
```

### Blockchain

#### Register on Blockchain
```http
POST /api/blockchain/register
Authorization: Bearer <token>
Content-Type: application/json

{
  "investigation_id": "uuid"
}

Response: 200 OK
{
  "id": "uuid",
  "report_id": "uuid",
  "report_hash": "sha256_hash",
  "transaction_hash": "0x...",
  "block_number": 123456,
  "chain_id": 11155111,
  "submitter_address": "0x...",
  "verified": true,
  "registered_at": "2024-01-01T00:00:00Z"
}
```

#### Verify Report Hash
```http
POST /api/blockchain/verify
Content-Type: application/json

{
  "report_hash": "64_character_sha256_hash"
}

Response: 200 OK
{
  "valid": true,
  "on_chain": true,
  "hash_match": true,
  "registered_at": "2024-01-01T00:00:00Z",
  "transaction_hash": "0x...",
  "message": "Report hash verified on blockchain"
}
```

## Error Responses

```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

### Status Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Rate Limiting

- Default: 60 requests per minute per user
- Burst: Up to 100 requests in short bursts
- Headers returned:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`
