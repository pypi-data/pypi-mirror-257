from typing import List, Optional, TypedDict

import httpx

from pflops.auth import get_local_token
from pflops.constant import API_BASE_URL


def _auth_client() -> httpx.Client:
    token = get_local_token()
    return httpx.Client(
        headers={"authorization": f"Bearer {token}"},
        base_url=API_BASE_URL,
        timeout=10,
    )


def retrieve_token(cli_id: str) -> Optional[str]:
    r = httpx.get(f"{API_BASE_URL}/cli/auth/check?id={cli_id}")
    try:
        data = r.raise_for_status().json()
        return data["token"]
    except httpx.HTTPStatusError:
        return None


def retrieve_user():
    r = _auth_client().get("/user")
    return r.raise_for_status().json()


def retrieve_org():
    r = _auth_client().get("/org")
    return r.raise_for_status().json()


def list_datasets():
    r = _auth_client().get("/datasets")
    return r.raise_for_status().json()


def create_dataset(name: str, size: int):
    r = _auth_client().post(
        "/datasets",
        json={"name": name, "size": size},
    )
    return r.raise_for_status().json()


def retrieve_dataset(name: str):
    r = _auth_client().get(f"/datasets/{name}")
    return r.raise_for_status().json()


def delete_dataset(name: str):
    r = _auth_client().delete(f"/datasets/{name}")
    return r.raise_for_status().json()


def finish_upload_dataset(name: str, upload_id: str, e_tags: List[str]):
    r = _auth_client().post(
        f"/datasets/{name}/upload/finish",
        json={"uploadId": upload_id, "eTags": e_tags},
    )
    return r.raise_for_status().json()
