import sys
import os
import traceback

# Tambahkan path root repository ke sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from main import app
except Exception as e:
    print("=== UNHANDLED IMPORT ERROR IN MAIN.PY ===")
    print(traceback.format_exc())
    print("=========================================")
    raise e