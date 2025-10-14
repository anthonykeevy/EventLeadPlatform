# EventLead Platform

**Multi-Tenant SaaS for Event Lead Collection**

Beautiful, branded lead collection forms for events. Drag-and-drop form builder with custom backgrounds.

---

## 🎯 Project Status

- ✅ Planning Complete (PRD, UX Spec, Project Analysis)
- ✅ Solution Architecture Complete (43 technologies, 13 database tables, 60+ API endpoints)
- ✅ Cohesion Check Complete (100% ready for implementation)
- ✅ Development Environment Setup Complete
- ⏳ Epic 1 (Authentication & Onboarding) - Ready to start

**Timeline:** 22 weeks (5.5 months)  
**Developer:** Anthony Keevy (Solo Founder)  
**Methodology:** BMAD v6 (Agentic Development)

---

## 📚 Documentation

- **PRD:** `docs/prd.md` - Product requirements, business model, compliance
- **UX Specification:** `docs/ux-specification.md` - Design system, 50+ screens, 20 components
- **Solution Architecture:** `docs/solution-architecture.md` - Complete architecture (7,267 lines)
- **Cohesion Check:** `docs/architecture-cohesion-check.md` - Validation report (100% ready)
- **Setup Guide:** `docs/development-setup-guide.md` - Environment setup instructions

---

## 🛠️ Tech Stack

**Frontend:**
- React 18.2.0 + TypeScript 5.2.2
- Vite 5.0.0 (build tool)
- Tailwind CSS 3.3.5 (styling)
- Zustand 4.4.6 (state management)
- dnd-kit 6.0.8 (drag-and-drop form builder)
- TanStack Query 5.8.4 (data fetching)
- Framer Motion 10.16.5 (animations)

**Backend:**
- FastAPI 0.119.0 (async Python web framework)
- SQLAlchemy 2.0.44 (ORM)
- Alembic 1.17.0 (database migrations)
- Python 3.13 (language)

**Database:**
- Microsoft SQL Server 2022 (local dev)
- Azure SQL Database (production)

**Infrastructure:**
- Docker 28.4.0 (MailHog email testing)
- Git 2.49.0 (version control)
- Azure Cloud (production hosting)

---

## 🚀 Quick Start

### Automated Service Management
```powershell
# Start all services and check dependencies
.\scripts\start-services-clean.ps1

# Monitor service status
.\scripts\simple-monitor.ps1

# View service logs
.\scripts\view-logs.ps1 -Service all
```

### Manual Service Startup

#### 1. Start MailHog (Email Testing)
```powershell
docker-compose up mailhog -d
```
MailHog runs at: http://localhost:8025

#### 2. Start Backend
```powershell
cd backend
.\venv\Scripts\activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Backend runs at: http://localhost:8000

#### 3. Start Frontend (New Terminal)
```powershell
cd frontend
npm run dev
```
Frontend runs at: http://localhost:3000

### Service URLs
- **Frontend:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs (Swagger UI)
- **MailHog:** http://localhost:8025 (Email testing)
- **Database Test:** http://localhost:8000/api/test-database

---

## 📂 Project Structure

```
EventLeadPlatform/
├── backend/                    # FastAPI Python backend
│   ├── modules/               # Business logic modules (by Epic)
│   │   ├── auth/             # Epic 1: Authentication
│   │   ├── companies/        # Epic 2: Company management
│   │   ├── events/           # Epic 3: Events
│   │   ├── team/             # Epic 4: Team collaboration
│   │   ├── forms/            # Epic 5 & 6: Form builder & publishing
│   │   ├── payments/         # Epic 7: Payments & billing
│   │   ├── analytics/        # Epic 8: Lead collection & analytics
│   │   ├── images/           # Image management
│   │   └── audit/            # Epic 9: Audit trail
│   ├── models/               # SQLAlchemy ORM models
│   ├── common/               # Shared infrastructure
│   ├── tests/                # Backend tests
│   ├── main.py               # FastAPI app entry point
│   └── requirements.txt      # Python dependencies
│
├── frontend/                   # React SPA
│   ├── src/
│   │   ├── components/       # Shared UI components
│   │   ├── features/         # Feature-specific components (by Epic)
│   │   ├── lib/              # Utilities
│   │   ├── store/            # Zustand state management
│   │   └── pages/            # Route components
│   ├── package.json          # Node.js dependencies
│   └── vite.config.ts        # Vite configuration
│
├── database/                   # Database management
│   ├── migrations/           # Alembic migration files
│   ├── seeds/                # Seed data scripts
│   └── scripts/              # Database utility scripts
│
├── docs/                       # Project documentation
│   ├── prd.md
│   ├── ux-specification.md
│   ├── solution-architecture.md
│   └── architecture-cohesion-check.md
│
└── bmad/                       # BMAD custom agents
    └── agents/
        ├── database-migration-validator/  # Solomon (validates migrations)
        └── epic-boundary-guardian/        # Sentinel (enforces boundaries)
```

---

## 🧙 Guardian Agents

**Custom agents to prevent v4 pain points:**

### Solomon - SQL Standards Sage 📜
Validates database migrations against enterprise naming standards.

```powershell
@bmad/agents/database-migration-validator
*validate-migration    # Validate single migration
*check-standards       # Display database standards
*generate-template     # Generate compliant migration template
```

### Sentinel - Epic Boundary Guardian 🛡️
Prevents cross-epic code modifications (protects completed work).

```powershell
@bmad/agents/epic-boundary-guardian
*validate-changes      # Check changes don't cross epic boundaries
*show-boundaries       # Display current forbidden zones
*mark-epic-complete    # Mark epic complete (creates protected zone)
```

---

## 🏗️ Development Workflow

**Daily workflow:**

1. Start services
2. Work on story
3. Validate with guardian agents
4. Commit clean code

**Starting Epic 1 (Authentication):**
```powershell
# 1. Generate first story
@bmad/bmm/agents/sm
*create-story
Epic: Epic 1 - Authentication & Onboarding

# 2. Implement story
@bmad/bmm/agents/dev
*dev-story

# 3. Validate migration (if database changes)
@bmad/agents/database-migration-validator
*validate-migration

# 4. Validate boundaries
@bmad/agents/epic-boundary-guardian
*validate-changes

# 5. Commit
git add .
git commit -m "Epic 1, Story 1.1: User signup with email verification"
```

---

## 📊 Project Scope

- **Level:** 4 (Enterprise Platform)
- **Epics:** 9 major epics
- **Stories:** 62-83 estimated stories
- **Timeline:** 22 weeks (5.5 months)
- **Database Tables:** 13 core tables
- **API Endpoints:** 60+ endpoints
- **Technologies:** 43 tools with exact versions

---

## 🎓 Learning Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **React Docs:** https://react.dev/
- **SQL Server Docs:** https://learn.microsoft.com/en-us/sql/sql-server/
- **Tailwind CSS:** https://tailwindcss.com/docs
- **dnd-kit:** https://docs.dndkit.com/

---

## 📝 License

Proprietary - EventLead Platform

---

**Built with BMAD v6** - Agentic Development Methodology  
**Creator:** Anthony Keevy  
**Date:** October 2025

