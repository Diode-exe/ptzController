"""This script compiles the Cython modules for the ptzController project.
It uses the setup.py script to build the Cython extensions in place."""

import subprocess
import sys

def compile():
    """Compiles the Cython modules using the setup.py script."""
    subprocess.run([sys.executable, "setup.py", "build_ext", "--inplace"], check=True)
    
if __name__ == "__main__":
    compile()