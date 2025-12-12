"""
EventLead Platform - FastAPI Backend
Main application entry point
"""
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Import middleware and exception handlers
from middleware import RequestLoggingMiddleware, EnhancedRequestLoggingMiddleware, BulletproofRequestLoggingMiddleware, JWTAuthMiddleware, global_exception_handler
from middleware.test_middleware import TestMiddleware
from common.logger import configure_logging

# Import routers
from modules.auth import auth_router
from modules.users.router import router as users_router
from modules.companies.router import router as companies_router
from modules.invitations.router import router as invitations_router
from modules.config.router import router as config_router, admin_router as config_admin_router
from modules.countries.router import router as countries_router
from modules.dashboard.router import router as dashboard_router
from modules.events.router import router as events_router
from modules.admin.dashboard_router import router as admin_dashboard_router  # Story 2.6
from modules.events.admin_review_router import router as admin_review_router  # Story 2.6
from modules.forms.router import router as forms_router  # Story 2.8: Form Header Foundation
from modules.forms.access_control_router import router as forms_access_control_router  # Story 2.9: Form Access Control
from modules.forms.ownership_router import router as forms_ownership_router  # Story 2.9: Form Ownership Transfer
from modules.forms.public_router import router as forms_public_router  # Story 2.12: External Approver Support
from modules.forms.version_router import versions_router, active_version_router  # Story 3.1: Form Versioning
from modules.audit.router import router as audit_router  # Story 2.13: Audit Trail & Compliance
from modules.fonts.router import router as fonts_router  # Google Fonts caching

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
# Story 0.2: Automatic error logging - catches ALL exceptions including HTTPException
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, global_exception_handler)  # Catches 4xx/5xx errors

# Add middleware (LIFO order - last added runs first)
# 1. JWT authentication middleware (validates tokens and injects current user)
app.add_middleware(JWTAuthMiddleware)

# 2. CORS middleware (allow frontend to call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://127.0.0.1:3000",  # React dev server (IPv4)
        "http://localhost:5173",  # Vite default port (backup)
        "http://127.0.0.1:5173",  # Vite default port (IPv4)
        # Add current origin for safety if user is accessing via explicit IP or different port
        "*"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],  # Explicitly allow all methods including OPTIONS
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(companies_router)
app.include_router(invitations_router)
app.include_router(config_router)  # Story 1.13: Public configuration
app.include_router(config_admin_router)  # Story 1.13: Admin configuration management
app.include_router(countries_router)  # Story 1.12: Country validation
app.include_router(dashboard_router)  # Story 1.18: Dashboard KPIs
app.include_router(events_router)  # Story 2.4: Event Management CRUD
app.include_router(admin_dashboard_router, prefix="/api")  # Story 2.6: Admin Dashboard
app.include_router(admin_review_router, prefix="/api")  # Story 2.6: Admin Review
# Register access_control_router FIRST to ensure specific routes (access-types, relationship-types) 
# are matched before parameterized routes ({form_id}) in forms_router
app.include_router(forms_access_control_router)  # Story 2.9: Form Access Control
app.include_router(forms_ownership_router)  # Story 2.9: Form Ownership Transfer
app.include_router(forms_public_router)  # Story 2.12: External Approver Support
app.include_router(versions_router)  # Story 3.1: Form Versioning
app.include_router(active_version_router)  # Story 3.1: Form Versioning - Live/Active Endpoint
app.include_router(forms_router)  # Story 2.8: Form Header Foundation
app.include_router(audit_router, prefix="/api")  # Story 2.13: Audit Trail & Compliance
app.include_router(fonts_router)  # Google Fonts caching

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

# 3. Test middleware (simple test)
print("Registering TestMiddleware...")
try:
    app.add_middleware(TestMiddleware)
    print("TestMiddleware registered successfully")
except Exception as e:
    print(f"ERROR registering TestMiddleware: {e}")
    import traceback
    print(f"Traceback: {traceback.format_exc()}")

# 4. Bulletproof request logging middleware (guaranteed payload capture)
# Note: FastAPI add_middleware doesn't support keyword args, so debug is set in the class
print("Registering BulletproofRequestLoggingMiddleware...")
try:
    app.add_middleware(BulletproofRequestLoggingMiddleware)
    print("BulletproofRequestLoggingMiddleware registered successfully")
except Exception as e:
    print(f"ERROR registering BulletproofRequestLoggingMiddleware: {e}")
    import traceback
    print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    import uvicorn
    
    print("Starting EventLead Platform API...")
    print("API Docs: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/api/health")
    print("Database Test: http://localhost:8000/api/test-database")
    print("")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Hot reload on code changes
        log_level="info"
    )

