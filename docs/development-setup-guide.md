# Development Environment Setup Guide

**Project:** EventLeadPlatform  
**OS:** Windows 10/11  
**Date:** 2025-10-12  
**Target:** Local development environment (Azure production later)

---

## Prerequisites Checklist

Before starting development, you need these tools installed:

- [ ] Python 3.11.6
- [ ] Node.js 18+ (with npm)
- [ ] SQL Server 2022 (local install OR Docker container)
- [ ] Docker Desktop (for MailHog email testing)
- [ ] Git (version control)
- [ ] VS Code or Cursor IDE (recommended)
- [ ] Postman or Thunder Client (API testing - optional)

**Estimated Setup Time:** 1-2 hours (depending on internet speed for downloads)

---

## Step 1: Install Python 3.11.6

### Download Python

**Option A: Official Python Installer (Recommended)**

1. Visit: https://www.python.org/downloads/
2. Download: Python 3.11.6 (Windows installer)
3. Run installer
4. ✅ **CRITICAL:** Check "Add Python 3.11 to PATH" (enables command line)
5. Click "Install Now"

**Verify Installation:**
```powershell
python --version
# Should show: Python 3.11.6

pip --version
# Should show: pip 23.x.x (from Python 3.11)
```

**Option B: Microsoft Store**
```powershell
# Search "Python 3.11" in Microsoft Store
# Click Install
```

### Setup Virtual Environment Tool

```powershell
# Install virtualenv (for isolated project environments)
pip install virtualenv

# Verify
virtualenv --version
```

---

## Step 2: Install Node.js 18+

### Download Node.js

1. Visit: https://nodejs.org/
2. Download: LTS version (18.x or 20.x)
3. Run installer
4. Accept defaults (includes npm package manager)
5. Click "Install"

**Verify Installation:**
```powershell
node --version
# Should show: v18.x.x or v20.x.x

npm --version
# Should show: 9.x.x or 10.x.x
```

---

## Step 3: Install SQL Server 2022

You have two options: Local install (full featured) or Docker container (simpler).

### Option A: SQL Server 2022 Local Install (Recommended for Production-Like Environment)

**Download:**
1. Visit: https://www.microsoft.com/en-us/sql-server/sql-server-downloads
2. Download: SQL Server 2022 Developer Edition (FREE)
3. Run installer

**Installation Steps:**
1. Select: "Basic" installation (simplest for development)
2. Accept license
3. Choose installation location (default is fine)
4. Click "Install"
5. Wait 10-20 minutes (downloads and installs)

**Install SQL Server Management Studio (SSMS) - Optional but Helpful:**
1. After SQL Server installs, installer offers SSMS
2. Click "Install SSMS" or download separately
3. SSMS is a GUI for managing databases (easier than command line)

**Verify Installation:**
```powershell
# Test connection
sqlcmd -S localhost -E -Q "SELECT @@VERSION"

# Should show: Microsoft SQL Server 2022...
```

**Create EventLeadPlatform Database:**
```sql
-- In SSMS or sqlcmd:
CREATE DATABASE EventLeadPlatform;
GO

-- Verify
SELECT name FROM sys.databases WHERE name = 'EventLeadPlatform';
```

---

### Option B: SQL Server Docker Container (Simpler, Containerized)

**Prerequisites:** Docker Desktop must be installed first (see Step 4)

```powershell
# Pull SQL Server 2022 image
docker pull mcr.microsoft.com/mssql/server:2022-latest

# Run SQL Server container
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=YourStrong!Passw0rd" `
  -p 1433:1433 --name sqlserver2022 `
  -d mcr.microsoft.com/mssql/server:2022-latest

# Verify running
docker ps
# Should show: sqlserver2022 container running

# Connect and create database
docker exec -it sqlserver2022 /opt/mssql-tools/bin/sqlcmd `
  -S localhost -U SA -P "YourStrong!Passw0rd"

# In sqlcmd:
CREATE DATABASE EventLeadPlatform;
GO
```

**Connection String (for .env.local):**
```
DATABASE_URL=mssql+pyodbc://SA:YourStrong!Passw0rd@localhost:1433/EventLeadPlatform?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes
```

---

## Step 4: Install Docker Desktop

**Download:**
1. Visit: https://www.docker.com/products/docker-desktop
2. Download: Docker Desktop for Windows
3. Run installer
4. Restart computer (required)

**Verify Installation:**
```powershell
docker --version
# Should show: Docker version 24.x.x

docker-compose --version
# Should show: Docker Compose version 2.x.x
```

**Enable WSL 2 (If Prompted):**
- Docker may ask to enable WSL 2 (Windows Subsystem for Linux)
- Follow prompts to install
- This is normal and recommended

---

## Step 5: Install Git

**Download:**
1. Visit: https://git-scm.com/download/win
2. Download: Git for Windows
3. Run installer
4. Accept defaults (recommended settings)

**Verify Installation:**
```powershell
git --version
# Should show: git version 2.x.x
```

**Configure Git (First Time Only):**
```powershell
git config --global user.name "Anthony Keevy"
git config --global user.email "your-email@example.com"

# Verify
git config --list
```

---

## Step 6: Setup MailHog (Email Testing)

**What is MailHog?**
A local email testing server that catches emails without sending them. You can view emails in a web UI.

**Run MailHog Container:**
```powershell
# Pull MailHog image
docker pull mailhog/mailhog

# Run MailHog
docker run -d -p 1025:1025 -p 8025:8025 --name mailhog mailhog/mailhog

# Verify running
docker ps
# Should show: mailhog container running
```

**Access MailHog Web UI:**
- Open browser: http://localhost:8025
- You should see MailHog interface (empty inbox initially)
- When your app sends emails (verification, invitations), they appear here

**SMTP Connection (for .env.local):**
```
SMTP_HOST=localhost
SMTP_PORT=1025
```

---

## Step 7: Clone/Create Project Repository

### Option A: If Repository Already Exists (GitHub)

```powershell
# Navigate to projects folder
cd C:\Users\tonyk\OneDrive\Projects\

# Clone repository
git clone https://github.com/yourusername/EventLeadPlatform.git

# Enter project
cd EventLeadPlatform
```

### Option B: Create New Repository (Fresh Start)

```powershell
# Navigate to projects folder
cd C:\Users\tonyk\OneDrive\Projects\EventLeadPlatform

# Initialize Git
git init

# Create .gitignore
echo "node_modules/" > .gitignore
echo "venv/" >> .gitignore
echo ".env.local" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".DS_Store" >> .gitignore

# Initial commit
git add .
git commit -m "Initial commit"
```

---

## Step 8: Create Project Structure

**Create folder structure from architecture:**

```powershell
# Backend folders
mkdir backend
mkdir backend\modules
mkdir backend\modules\auth
mkdir backend\modules\companies
mkdir backend\modules\events
mkdir backend\modules\team
mkdir backend\modules\forms
mkdir backend\modules\payments
mkdir backend\modules\analytics
mkdir backend\modules\images
mkdir backend\modules\audit
mkdir backend\common
mkdir backend\common\logging
mkdir backend\common\middleware
mkdir backend\common\providers
mkdir backend\common\utils
mkdir backend\models
mkdir backend\tests

# Frontend folders
mkdir frontend
mkdir frontend\src
mkdir frontend\src\components
mkdir frontend\src\features
mkdir frontend\src\lib
mkdir frontend\src\store
mkdir frontend\src\pages
mkdir frontend\public

# Database folders
mkdir database
mkdir database\migrations
mkdir database\migrations\versions
mkdir database\seeds
mkdir database\scripts

# Already have docs/ from architecture work
# docs/prd.md, docs/ux-specification.md, docs/solution-architecture.md exist
```

---

## Step 9: Install Backend Dependencies

**Create requirements.txt:**

```powershell
# Navigate to backend folder
cd backend

# Create requirements.txt
```

Create file `backend/requirements.txt`:
```txt
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0  # ASGI server for FastAPI
pydantic==2.5.0

# Database
sqlalchemy==2.0.23
alembic==1.12.1
pyodbc==5.0.1

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.1.1

# HTTP & External APIs
httpx==0.25.2
stripe==7.6.0

# Azure SDKs
azure-storage-blob==12.19.0
azure-communication-email==1.2.0

# Logging & Monitoring
structlog==23.2.0
opencensus-ext-azure==1.1.13

# Environment & Config
python-decouple==3.8

# Image Processing
Pillow==10.1.0

# PDF Generation
reportlab==4.0.7

# CSV Generation
pandas==2.1.3

# File Operations
aiofiles==23.2.1

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1

# Development
black==23.11.0  # Code formatting
flake8==6.1.0   # Linting
```

**Install Dependencies:**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate again
.\venv\Scripts\Activate.ps1

# Your prompt should now show (venv)

# Install all dependencies
pip install -r requirements.txt

# This takes 5-10 minutes
```

**Verify Installation:**
```powershell
# Check FastAPI installed
python -c "import fastapi; print(fastapi.__version__)"
# Should show: 0.104.1

# Check SQLAlchemy
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
# Should show: 2.0.23
```

---

## Step 10: Install Frontend Dependencies

**Create package.json:**

```powershell
# Navigate to frontend folder
cd ..\frontend  # From backend folder

# Create package.json
```

Create file `frontend/package.json`:
```json
{
  "name": "eventlead-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "vitest"
  },
  "dependencies": {
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "react-router-dom": "6.20.0",
    "zustand": "4.4.6",
    "react-hook-form": "7.48.2",
    "@dnd-kit/core": "6.0.8",
    "@dnd-kit/sortable": "7.0.2",
    "@dnd-kit/utilities": "3.2.1",
    "@tanstack/react-query": "5.8.4",
    "axios": "1.6.2",
    "recharts": "2.10.1",
    "date-fns": "2.30.0",
    "lucide-react": "0.294.0",
    "@radix-ui/react-dialog": "1.0.5",
    "@radix-ui/react-dropdown-menu": "2.0.6",
    "@radix-ui/react-select": "2.0.0",
    "framer-motion": "10.16.5",
    "browser-image-compression": "2.0.2"
  },
  "devDependencies": {
    "@types/react": "18.2.37",
    "@types/react-dom": "18.2.15",
    "@vitejs/plugin-react": "4.2.0",
    "typescript": "5.2.2",
    "vite": "5.0.0",
    "tailwindcss": "3.3.5",
    "autoprefixer": "10.4.16",
    "postcss": "8.4.31",
    "vitest": "1.0.4",
    "@testing-library/react": "14.1.2",
    "@testing-library/jest-dom": "6.1.5",
    "eslint": "8.54.0",
    "prettier": "3.1.0"
  }
}
```

**Install Dependencies:**
```powershell
# Make sure you're in frontend/ folder
npm install

# This takes 3-5 minutes (downloads ~300MB of node_modules)
```

**Verify Installation:**
```powershell
# Check React installed
npm list react
# Should show: react@18.2.0

# Check Vite
npm list vite
# Should show: vite@5.0.0
```

---

## Step 11: Configure Environment Variables

### Create .env.example (Template)

Create file `.env.example` in project root:
```bash
# Database
DATABASE_URL=mssql+pyodbc://localhost/EventLeadPlatform?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes

# Environment
ENVIRONMENT=development

# JWT Secret (generate your own - DO NOT use this in production)
JWT_SECRET_KEY=your-secret-key-change-this-in-production-min-32-chars

# Email (MailHog for dev)
SMTP_HOST=localhost
SMTP_PORT=1025
EMAIL_FROM=noreply@eventlead.local

# Storage (Local for dev)
STORAGE_TYPE=local
LOCAL_STORAGE_PATH=./local_storage

# Stripe (Test mode)
STRIPE_SECRET_KEY=sk_test_your_stripe_test_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here

# Logging
LOG_LEVEL=DEBUG
LOG_API_REQUESTS=true
LOG_REQUEST_BODY=true
LOG_DATABASE_QUERIES=true

# Frontend URL (CORS)
FRONTEND_URL=http://localhost:3000

# Backend URL
BACKEND_URL=http://localhost:8000
```

### Create .env.local (Actual Config - Not in Git)

```powershell
# Copy template to actual config
cp .env.example .env.local

# Edit .env.local with your actual values
# This file is gitignored (contains secrets)
```

**For now, defaults are fine.** You'll add Stripe keys when you get to Epic 7.

---

## Step 12: Initialize Database with Alembic

### Setup Alembic (Database Migrations)

**Create Alembic config:**

```powershell
# Navigate to project root
cd C:\Users\tonyk\OneDrive\Projects\EventLeadPlatform

# Activate Python venv
.\backend\venv\Scripts\Activate.ps1

# Initialize Alembic
cd database
alembic init migrations

# This creates:
# database/migrations/
#   alembic.ini
#   env.py
#   script.py.mako
#   versions/
```

**Configure Alembic to use your database:**

Edit `database/migrations/env.py`:
```python
# Add at top
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from backend.database import Base  # Your SQLAlchemy Base
from backend.models import *  # Import all models
from decouple import config

# Update target_metadata
target_metadata = Base.metadata

# Update sqlalchemy.url
def get_url():
    return config("DATABASE_URL")

# In run_migrations_offline() and run_migrations_online()
# Use: url=get_url()
```

**Create Initial Migration (When Ready):**
```powershell
# After you create SQLAlchemy models
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

---

## Step 13: Create Docker Compose (All Services Together)

**Create docker-compose.yml in project root:**

```yaml
version: '3.8'

services:
  # MailHog - Email Testing
  mailhog:
    image: mailhog/mailhog:latest
    ports:
      - "1025:1025"  # SMTP port
      - "8025:8025"  # Web UI port
    container_name: eventlead-mailhog
    
  # SQL Server (Optional - if not using local install)
  # sqlserver:
  #   image: mcr.microsoft.com/mssql/server:2022-latest
  #   environment:
  #     - ACCEPT_EULA=Y
  #     - SA_PASSWORD=YourStrong!Passw0rd
  #   ports:
  #     - "1433:1433"
  #   container_name: eventlead-sqlserver
  #   volumes:
  #     - sqlserver-data:/var/opt/mssql

# volumes:
#   sqlserver-data:
```

**Start All Services:**
```powershell
# From project root
docker-compose up -d

# Verify
docker-compose ps
# Should show: mailhog running (and sqlserver if uncommented)

# Stop services
docker-compose down

# Start again when needed
docker-compose up -d
```

---

## Step 14: Create Minimal FastAPI Backend (Smoke Test)

**Create backend/main.py:**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="EventLead Platform API",
    version="1.0.0",
    description="Multi-tenant SaaS for event lead collection"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "EventLead Platform API",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    return {"message": "EventLead Platform API - Ready"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

**Run Backend:**
```powershell
# Activate venv (if not already)
cd backend
.\venv\Scripts\Activate.ps1

# Run FastAPI
python main.py

# Should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
```

**Test Backend:**
- Open browser: http://localhost:8000
- Should see: `{"message": "EventLead Platform API - Ready"}`
- Open: http://localhost:8000/docs
- Should see: Swagger UI (auto-generated API docs)

**✅ Backend working!** Press Ctrl+C to stop.

---

## Step 15: Create Minimal React Frontend (Smoke Test)

**Create frontend/index.html:**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>EventLead Platform</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

**Create frontend/src/main.tsx:**

```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

**Create frontend/src/App.tsx:**

```typescript
import React from 'react'

function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-teal-600 mb-4">
          EventLead Platform
        </h1>
        <p className="text-gray-600">
          Development Environment Ready ✅
        </p>
      </div>
    </div>
  )
}

export default App
```

**Create frontend/src/index.css:**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**Create frontend/vite.config.ts:**

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

**Create frontend/tsconfig.json:**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

**Create frontend/tailwind.config.js:**

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#14B8A6', // teal-500
        },
        secondary: {
          DEFAULT: '#8B5CF6', // violet-500
        },
      },
    },
  },
  plugins: [],
}
```

**Run Frontend:**
```powershell
# From frontend/ folder
npm run dev

# Should see:
# VITE v5.0.0 ready in XXX ms
# ➜ Local: http://localhost:3000/
```

**Test Frontend:**
- Open browser: http://localhost:3000
- Should see: "EventLead Platform - Development Environment Ready ✅"

**✅ Frontend working!** Press Ctrl+C to stop.

---

## Step 16: Verify Complete Environment

**Run ALL services together:**

```powershell
# Terminal 1: Start Docker services
docker-compose up -d

# Terminal 2: Start Backend
cd backend
.\venv\Scripts\Activate.ps1
python main.py

# Terminal 3: Start Frontend
cd frontend
npm run dev
```

**Access Points:**
- Frontend: http://localhost:3000 (React app)
- Backend API: http://localhost:8000 (FastAPI)
- API Docs: http://localhost:8000/docs (Swagger UI)
- MailHog: http://localhost:8025 (Email viewer)

**✅ Full Environment Running!**

---

## Common Issues & Fixes

### Issue 1: Python not found

**Error:** `'python' is not recognized as an internal or external command`

**Fix:**
- Python not in PATH
- Reinstall Python with "Add to PATH" checked
- OR manually add to PATH: `C:\Users\tonyk\AppData\Local\Programs\Python\Python311`

---

### Issue 2: Docker not starting

**Error:** `Docker Desktop failed to start`

**Fix:**
- Ensure Hyper-V enabled (Windows feature)
- Ensure WSL 2 installed
- Restart computer
- Run Docker Desktop as Administrator

---

### Issue 3: SQL Server connection failed

**Error:** `Cannot connect to SQL Server`

**Fix:**
- Check SQL Server running: `services.msc` → Find "SQL Server (MSSQLSERVER)" → Should be "Running"
- Check ODBC Driver installed: Download "ODBC Driver 18 for SQL Server"
- Check connection string in .env.local

---

### Issue 4: npm install fails

**Error:** `npm ERR! code ERESOLVE`

**Fix:**
```powershell
# Use legacy peer deps
npm install --legacy-peer-deps
```

---

### Issue 5: Virtual environment activation fails

**Error:** `Execution of scripts is disabled on this system`

**Fix:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Next Steps After Environment Setup

**Once environment is working:**

1. ✅ **Verify smoke tests** (backend and frontend both running)
2. ✅ **Create first SQLAlchemy model** (User table)
3. ✅ **Generate first migration** (with Solomon's validation)
4. ✅ **Create first API endpoint** (/api/auth/signup)
5. ✅ **Create first React component** (SignupForm)
6. ✅ **Start Epic 1 implementation** (Authentication & Onboarding)

---

## Development Workflow (Daily)

**Starting work:**
```powershell
# 1. Start Docker services (MailHog, SQL Server if using Docker)
docker-compose up -d

# 2. Start Backend (Terminal 1)
cd backend
.\venv\Scripts\Activate.ps1
python main.py

# 3. Start Frontend (Terminal 2)
cd frontend
npm run dev

# 4. Open browser
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
# MailHog: http://localhost:8025
```

**Ending work:**
```powershell
# Stop backend: Ctrl+C in Terminal 1
# Stop frontend: Ctrl+C in Terminal 2
# Stop Docker: docker-compose down
```

---

## Tools Installed Summary

| Tool | Version | Purpose | Verify Command |
|------|---------|---------|----------------|
| Python | 3.11.6 | Backend language | `python --version` |
| pip | 23.x | Python package manager | `pip --version` |
| Node.js | 18.x/20.x | Frontend runtime | `node --version` |
| npm | 9.x/10.x | JavaScript package manager | `npm --version` |
| SQL Server | 2022 | Database | `sqlcmd -S localhost -E -Q "SELECT @@VERSION"` |
| Docker | 24.x | Containerization | `docker --version` |
| Git | 2.x | Version control | `git --version` |

**Total Install Time:** 1-2 hours  
**Disk Space Required:** ~5GB (Python, Node, Docker, SQL Server)

---

**Setup Guide Created By:** Winston (Architect Agent)  
**For:** Anthony Keevy  
**Date:** 2025-10-12  
**Status:** Ready to execute step-by-step

