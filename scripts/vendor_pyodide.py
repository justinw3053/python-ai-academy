import urllib.request
import os
import tarfile
import shutil

PYODIDE_VERSION = "0.26.1"
PYODIDE_URL = f"https://github.com/pyodide/pyodide/releases/download/{PYODIDE_VERSION}/pyodide-{PYODIDE_VERSION}.tar.bz2"
TARGET_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend", "pyodide")

def vendor_pyodide():
    if os.path.exists(TARGET_DIR):
        print("Pyodide already vendored.")
        return

    print(f"Downloading Pyodide {PYODIDE_VERSION}...")
    tar_path = "/tmp/pyodide.tar.bz2"
    
    req = urllib.request.Request(PYODIDE_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response, open(tar_path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    
    print("Extracting Pyodide...")
    with tarfile.open(tar_path, "r:bz2") as tar:
        tar.extractall(path="/tmp/")
        
    extracted_dir = f"/tmp/pyodide"
    print(f"Moving to {TARGET_DIR}...")
    shutil.move(extracted_dir, TARGET_DIR)
    
    print("Pyodide vendored successfully.")

if __name__ == "__main__":
    vendor_pyodide()
