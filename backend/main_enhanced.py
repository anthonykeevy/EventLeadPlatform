"""
EventLead Platform - FastAPI Backend with Enhanced Payload Capture
Main application entry point with ASGI middleware for payload logging
"""
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Import enhanced middleware and exception handlers
from middleware.enhanced_request_logger import EnhancedRequestLoggingMiddleware
from middleware import JWTAuthMiddleware, global_exception_handler
from common.logger import configure_logging

# Import routers
from modules.auth import auth_router
from modules.users.router import router as users_router
from modules.companies.router import router as companies_router
from modules.invitations.router import router as invitations_router
from modules.config.router import router as config_router, admin_router as config_admin_router
from modules.countries.router import router as countries_router
from modules.dashboard.router import router as dashboard_router

# Configure application-wide logging
configure_logging(log_level="INFO")

app = FastAPI(
    title="EventLead Platform API (Enhanced Logging)",
    version="1.0.0",
    description="Multi-tenant SaaS for event lead collection with enhanced payload capture",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
)

# Register global exception handler FIRST (catches all unhandled errors)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, global_exception_handler)

# Add enhanced ASGI middleware for payload capture
app.add_middleware(EnhancedRequestLoggingMiddleware)

# Add JWT authentication middleware
app.add_middleware(JWTAuthMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite default port (backup)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(companies_router)
app.include_router(invitations_router)
app.include_router(config_router)
app.include_router(config_admin_router)
app.include_router(countries_router)
app.include_router(dashboard_router)

@app.get("/")
async def root():
    """Root endpoint - confirms API is running"""
    return {
        "message": "EventLead Platform API (Enhanced Logging)",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "features": ["Enhanced payload capture", "ASGI middleware"]
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "EventLead Platform API (Enhanced)",
        "environment": "development"
    }

@app.post("/api/test-payload-capture")
async def test_payload_endpoint(request: Request):
    """Test endpoint for payload capture verification"""
    from fastapi import Request
    import json
    
    body = await request.body()
    return {
        "message": "Payload capture test successful",
        "received_data": json.loads(body) if body else None,
        "body_length": len(body),
        "timestamp": "2025-01-15T12:00:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting EventLead Platform API with Enhanced Logging...")
    print("📖 API Docs: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/api/health")
    print("🧪 Payload Test: http://localhost:8000/api/test-payload-capture")
    print("")
    
    uvicorn.run(
        "main_enhanced:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
