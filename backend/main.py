
# src.config should always be loaded at the top of main 
# Before anuything else
from src.config import env
from src.routes import routes

import sys

is_fast_api = sys.argv[0].endswith("fastapi")

if not is_fast_api:
    print("Run backend with 'fastapi' command")
    print("    e.g. 'fastapi dev main'")
