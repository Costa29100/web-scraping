import requests
import pandas as pd
from datetime import datetime
import sys

# ⚙️ Identifiants Pôle emploi 
CLIENT_ID = ""
CLIENT_SECRET = ""

# URL du token
URL_TOKEN = ""

# Délai maximal d’attente (en secondes)
TIMEOUT = 15


def get_token():
    """Récupère le token d'accès OAuth2"""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "api_offresdemploiv2 o2dsoffre"
    }

    try:
        r = requests.post(URL_TOKEN, headers=headers, data=data, timeout=TIMEOUT)
        r.raise_for_status()
        token = r.json()["access_token"]
        return token
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la récupération du token : {e}")
        print("→ Vérifie ta connexion Internet ou réessaie plus tard.")
        sys.exit(1)


def get_jobs(token, mots_cles="BTP", range_start=0, range_end=99, publiee_depuis=30):
    """Récupère les offres depuis l'API Pôle emploi"""
    url = "https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "motsCles": mots_cles,
        "range": f"{range_start}-{range_end}",
        "publieeDepuis": publiee_depuis
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
        r.raise_for_status()
        offres = r.json().get("resultats", [])
        return offres
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la récupération des offres : {e}")
        sys.exit(1)


def save_to_excel(jobs, filename="offres_pole_emploi.xlsx"):
    """Sauvegarde les offres dans un fichier Excel"""
    if not jobs:
        print("⚠️ Aucune offre trouvée.")
        return

    data = []
    for job in jobs:
        data.append({
            "Intitulé": job.get("intitule", ""),
            "Entreprise": job.get("entreprise", {}).get("nom", ""),
            "Lieu": job.get("lieuTravail", {}).get("libelle", ""),
            "Date publication": job.get("dateCreation", ""),
            "Contrat": job.get("typeContrat", ""),
            "Description": job.get("description", ""),
            "URL": job.get("url", "")
        })

    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"✅ Fichier Excel créé : {filename}")


def main():
    print("🚀 Démarrage scraper Pôle emploi:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    print("🔑 Récupération du token...")
    token = get_token()
    print("✅ Token récupéré !")

    print("📡 Récupération des offres...")
    jobs = get_jobs(token, mots_cles="BTP", range_start=0, range_end=199, publiee_depuis=30)
    print(f"🔹 {len(jobs)} offres récupérées.")

    save_to_excel(jobs)


if __name__ == "__main__":
    main()
