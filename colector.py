import requests
import json
from datetime import datetime, timezone
import os
import sys

URL = "https://www.meteoromania.ro/wp-json/meteoapi/v2/starea-vremii"

ORE_CLIMATOLOGICE_UTC = [0, 6, 12, 18]

def colecteaza_date():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    date_meteo = response.json()

    # Ora observației din API
    obs_time = datetime.fromisoformat(date_meteo["date"])

    ora_utc = obs_time.astimezone(timezone.utc).hour

    if ora_utc not in ORE_CLIMATOLOGICE_UTC:
        print(
            f"Observația este de la {ora_utc:02d}:00 UTC. "
            "Nu este o observație climatologică. Omit salvarea."
        )
        sys.exit(0)

    os.makedirs("arhiva_anm_oficial", exist_ok=True)

    timestamp = (
        obs_time
        .astimezone(timezone.utc)
        .strftime("%Y-%m-%d_%H-%M_UTC")
    )

    fisier = f"arhiva_anm_oficial/meteo_romania_{timestamp}.json"

    # Evită dublurile
    if os.path.exists(fisier):
        print(f"Fișierul există deja: {fisier}")
        sys.exit(0)

    with open(fisier, "w", encoding="utf-8") as f:
        json.dump(date_meteo, f, ensure_ascii=False, indent=2)

    print(f"Salvat: {fisier}")

if __name__ == "__main__":
    colecteaza_date()
