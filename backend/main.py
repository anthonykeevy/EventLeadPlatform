"""
EventLead Platform - FastAPI Backend
Main application entry point
"""
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import middleware and exception handlers
from middleware import RequestLoggingMiddleware, JWTAuthMiddleware, global_exception_handler
from common.logger import configure_logging

# Import routers
from modules.auth import auth_router
from modules.users.router import router as users_router
from modules.companies.router import router as companies_router
from modules.invitations.router import router as invitations_router

# Configure application-wide logging
configure_logging(log_level="INFO")

app = FastAPI(
    title="EventLead Platform API",
    version="1.0.0",
    description="Multi-tenant SaaS for event lead collection",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
)

# Register global exception handler FIRST (catches all unhandled errors)
app.add_exception_handler(Exception, global_exception_handler)

# Add middleware (LIFO order - last added runs first)
# 1. Request logging middleware (logs all requests automatically)
app.add_middleware(RequestLoggingMiddleware)

# 2. JWT authentication middleware (validates tokens and injects current user)
app.add_middleware(JWTAuthMiddleware)

# 3. CORS middleware (allow frontend to call backend)
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

@app.get("/")
async def root():
    """Root endpoint - confirms API is running"""
    return {
        "message": "EventLead Platform API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "EventLead Platform API",
        "environment": "development"
    }

@app.get("/api/test-database")
async def test_database():
    """Test database connection"""
    try:
        import pyodbc  # type: ignore
        # Try to connect to SQL Server
        conn_str = (
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=localhost;"
            "Database=master;"  # Use master to test connection
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        conn.close()
        
        return {
            "status": "connected",
            "database": "SQL Server",
            "version": version[:100] + "..."  # Truncate long version string
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting EventLead Platform API...")
    print("📖 API Docs: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/api/health")
    print("💾 Database Test: http://localhost:8000/api/test-database")
    print("")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Hot reload on code changes
        log_level="info"
    )

