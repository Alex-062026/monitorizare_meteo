import requests
import json
from datetime import datetime, timezone
import os
import sys

URL = "https://www.meteoromania.ro/wp-json/meteoapi/v2/starea-vremii"

def colecteaza_date():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    date_meteo = response.json()

    obs_time = datetime.fromisoformat(date_meteo["date"])

    timestamp = (
        obs_time
        .astimezone(timezone.utc)
        .strftime("%Y-%m-%d_%H-%M_UTC")
    )

    os.makedirs("arhiva_anm_oficial", exist_ok=True)

    fisier = f"arhiva_anm_oficial/meteo_romania_{timestamp}.json"

    # Evită salvarea aceleiași observații de două ori
    if os.path.exists(fisier):
        print(f"Observația există deja: {fisier}")
        sys.exit(0)

    with open(fisier, "w", encoding="utf-8") as f:
        json.dump(date_meteo, f, ensure_ascii=False, indent=2)

    print(f"Salvat: {fisier}")

if __name__ == "__main__":
    colecteaza_date()
