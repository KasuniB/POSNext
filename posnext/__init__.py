__version__ = "0.0.1"
import sys
import os

# Add inner folder to path if not already present
inner_path = os.path.join(os.path.dirname(__file__), "posnext")
if inner_path not in sys.path:
    sys.path.insert(0, inner_path)
