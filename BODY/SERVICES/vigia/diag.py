import os
import sys

# Get the directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Current Directory: {current_dir}")

# Go up 3 levels to reach Holisto_Seed root
# Level 1: SERVICES
# Level 2: BODY
# Level 3: Holisto_Seed (the root that contains the BODY package)
target_path = os.path.abspath(os.path.join(current_dir, "../../.."))
print(f"Target Path (3 levels up): {target_path}")

# Check if the target path contains the 'BODY' directory
body_exists = os.path.exists(os.path.join(target_path, "BODY"))
print(f"Does 'BODY' exist at target? {body_exists}")

# Try to import
sys.path.append(target_path)
try:
    import BODY
    print("Import 'BODY' successful!")
except ImportError as e:
    print(f"Import 'BODY' failed: {e}")

# Check what's actually in that target directory
try:
    print(f"Contents of {target_path}:")
    print(os.listdir(target_path))
except Exception as e:
    print(f"Failed to list directory: {e}")
