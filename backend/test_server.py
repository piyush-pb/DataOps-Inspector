import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing imports...")
    from app.main import app
    print("✅ FastAPI app imported successfully")
    
    from app.core.config import settings
    print("✅ Settings imported successfully")
    
    from app.core.database import engine, Base
    print("✅ Database imported successfully")
    
    print("\n✅ All imports successful!")
    print("Server should be ready to start.")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc() 