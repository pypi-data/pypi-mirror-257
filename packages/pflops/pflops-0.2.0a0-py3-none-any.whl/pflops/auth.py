import os
from typing import Optional

from pflops.constant import CLERK_TOKEN_PATH, PFLOPS_DIR


def get_local_token() -> Optional[str]:
    try:
        with open(CLERK_TOKEN_PATH, "r") as f:
            return f.read().strip()
    except:
        return None


def save_local_token(token: str):
    os.makedirs(PFLOPS_DIR, exist_ok=True)
    with open(CLERK_TOKEN_PATH, "w+") as f:
        f.write(token)
