from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes_analyze import router as analyze_router
from app.api.routes_correlation import router as correlation_router
from app.api.routes_web3 import router as web3_router
from app.api.routes_demos import router as demos_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Intelligent Digital Threat Detection, TLS Trust Chain Auditing, and Decentralized Threat Intelligence Platform.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Sub-routers
app.include_router(analyze_router, prefix=settings.API_V1_STR)
app.include_router(correlation_router, prefix=settings.API_V1_STR)
app.include_router(web3_router, prefix=settings.API_V1_STR)
app.include_router(demos_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "platform": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "OPERATIONAL",
        "endpoints": {
            "docs": "/docs",
            "analyze_url": f"{settings.API_V1_STR}/analyze/url",
            "analyze_message": f"{settings.API_V1_STR}/analyze/message",
            "threat_graph": f"{settings.API_V1_STR}/threats/graph",
            "blockchain_verify": f"{settings.API_V1_STR}/blockchain/verify/{{hash}}",
            "demo_cases": f"{settings.API_V1_STR}/demo/cases"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "engines": {
            "url_analyzer": "READY",
            "tls_ca_auditor": "READY",
            "ai_scam_detector": "READY",
            "correlation_graph": "READY",
            "web3_registry": "READY"
        }
    }

