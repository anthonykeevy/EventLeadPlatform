"""
Verify that all models can be imported successfully.
Run this from the project root: python backend/verify_models.py
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from backend.models import get_model_count, __all__
    
    count = get_model_count()
    print(f"✓ Successfully loaded {count} models")
    print(f"✓ Models exported: {len(__all__)}")
    
    # Verify model count
    if count == 33:
        print("✓ Model count correct (33 models)")
    else:
        print(f"✗ Model count incorrect: expected 33, got {count}")
        sys.exit(1)
    
    # Try importing key models
    from backend.models import (
        User, Company, UserCompany,
        Country, UserStatus,
        AppSetting, ActivityLog, ApiRequest, ABRSearch
    )
    print("✓ Key models import successfully")
    
    # Check SQLAlchemy registration
    from backend.common.database import Base
    table_count = len(Base.metadata.tables)
    print(f"✓ SQLAlchemy registered {table_count} tables")
    
    print("\n✅ All models verified successfully!")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

