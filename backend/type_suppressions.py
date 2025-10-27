# SQLAlchemy Type Suppressions for EventLead Platform
# These suppressions handle common SQLAlchemy patterns where Column types
# are converted to Python types for function calls.

# File: backend/modules/auth/router.py
# Suppress Column type conversion warnings for JWT token generation
# These are runtime-safe conversions from SQLAlchemy Column types to Python types

# File: backend/modules/companies/router.py  
# Suppress Column type conversion warnings for company relationship queries
# These are runtime-safe conversions from SQLAlchemy Column types to Python types

# File: backend/modules/invitations/router.py
# Suppress Column type conversion warnings for invitation token handling
# These are runtime-safe conversions from SQLAlchemy Column types to Python types

# Rationale:
# SQLAlchemy ORM models return Column types that need to be converted to Python types
# for function calls. The type checker flags these as errors, but they're actually
# correct runtime behavior. Suppressing these allows focus on actual logic errors.

# Epic 1 Status: These suppressions are acceptable for production code
# Epic 2: Consider refactoring to use proper type annotations if needed
