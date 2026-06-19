import requests
import json
from datetime import datetime
import os

# ID-ul resursei pe care ai găsit-o tu
RESOURCE_ID = "7cda3992-50c4-41e2-b26e-e027705e17a0"
URL = f"https://data.gov.ro/api/3/action/datastore_search?resource_id={RESOURCE_ID}"

def colecteaza_open_data():
    try:
        # Interogăm API-ul oficial guvernamental
        raspuns = requests.get(URL, timeout=15)
        raspuns.raise_for_status()
        date_complete = raspuns.json()
        
        # Extragem doar înregistrările efective (stațiile și parametrii lor)
        if date_complete.get("success"):
            statie_date = date_complete["result"]["records"]
            
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            os.makedirs("arhiva_anm_oficial", exist_ok=True)
            
            nume_fisier = f"arhiva_anm_oficial/meteo_romania_{timestamp}.json"
            with open(nume_fisier, "w", encoding="utf-8") as f:
                json.dump(statie_date, f, indent=4, ensure_ascii=False)
                
            print(f"Succes! S-au salvat datele oficiale pentru stații în {nume_fisier}")
        else:
            print("API-ul a răspuns, dar parametrii nu au putut fi extrași.")
            
    except Exception as e:
        print(f"A apărut o eroare la descărcare: {e}")

if __name__ == "__main__":
    colecteaza_open_data()
