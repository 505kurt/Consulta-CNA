import requests

from typing import Optional, List


def fetch_oab(
    oab: Optional[str] = None,
    name: Optional[str] = None,
    uf: Optional[str] = None,
    categoria: Optional[str] = None,
    base_url: str = "http://localhost:8000"
) -> List[dict]:
    
    payload = {
        "oab": oab,
        "name": name,
        "uf": uf,
        "categoria": categoria
    }

    payload = {k: v for k, v in payload.items() if v is not None}

    response = requests.post(f"{base_url}/fetch_oab", json=payload)

    response.raise_for_status()

    return response.json()
