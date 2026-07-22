import sys
import os

# Memastikan root folder masuk ke sys.path supaya import internal project aman
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app