import os

# Lazy imports to avoid loading all dependencies at package import time
def main():
    from .main import main as _main
    return _main()

def manage():
    from .manage import manage as _manage
    return _manage()
