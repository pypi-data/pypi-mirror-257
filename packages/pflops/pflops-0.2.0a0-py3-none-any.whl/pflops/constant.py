import os
from pathlib import Path

from dotenv import dotenv_values

env_var = {**os.environ, **dotenv_values(".env")}

CONSOLE_URL = env_var.get("CONSOLE_URL", "http://app.petaflops.ai")
API_BASE_URL = env_var.get("API_BASE_URL", "https://app.petaflops.ai/api")

LOGIN_TIMEOUT_SECONDS = 120

# Paths
PFLOPS_DIR = Path.home() / ".pflops"
CLERK_TOKEN_PATH = Path.home() / ".pflops/token"
