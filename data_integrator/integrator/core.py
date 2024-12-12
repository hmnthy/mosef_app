import os
import pandas as pd
import datetime

# Répertoire contenant les fichiers raw
current_year = datetime.datetime.now().year
raw_files_dir = "../../archived/raw"
staged_file_path = f"../../archived/staged/staged_data_{current_year}.csv"

def get_latest_raw_file(directory):
    try:
        # Lister les fichiers qui commencent par "raw_data" et se terminent par ".csv"
        files = [os.path.join(directory, f) for f in os.listdir(directory) if f.startswith("raw_data") and f.endswith(".csv")]
        if not files:
            raise FileNotFoundError("No raw_data files found in the directory.")
        # Retourner le fichier avec la date de modification la plus récente
        return max(files, key=os.path.getmtime)
    except Exception as e:
        raise Exception(f"Error finding latest raw file: {e}")

try:
    raw_file_path = get_latest_raw_file(raw_files_dir)
    print(f"Latest raw file detected: {raw_file_path}")
except Exception as e:
    print(f"Error: {e}")
    exit(1)

# Lecture du fichier par chunksize (optimisation de la mémoire)
chunk_size = 10000
dtype_dict = {
    "Year": str,  # Année sous forme de chaîne
    "Pathology Level 1": str,  # Niveau 1 des pathologies
    "Pathology Level 2": str,  # Niveau 2 des pathologies
    "Pathology Level 3": str,  # Niveau 3 des pathologies
    "Topology": str,  # Topologie
    "Age Group (5 years)": str,  # Groupe d'âge (tranches de 5 ans)
    "Gender": str,  # Sexe
    "Region": str,  # Région géographique
    "Department": str,  # Département géographique
    "Patient Count (top)": int,  # Nombre de patients (topologie)
    "Total Population": int,  # Population totale
    "Prevalence": float,  # Prévalence sous forme flottante
    "Priority Level": str,  # Niveau de priorité
    "Age Group Label": str,  # Étiquette du groupe d'âge
    "Gender Label": str,  # Étiquette du sexe
    "Sorting": int  # Tri
}

print(f"Reading raw file from: {raw_file_path}")
try:
    chunks = []
    # Lire le fichier par morceaux (chunks)
    for chunk in pd.read_csv(raw_file_path, sep=";", header=0, skipinitialspace=True, encoding="utf-8", dtype=dtype_dict, chunksize=chunk_size):
        chunks.append(chunk)
    # Concaténer les morceaux pour former un DataFrame complet
    raw_file = pd.concat(chunks)
except Exception as e:
    print(f"Error reading raw file: {e}")
    exit(1)

# Renommage des colonnes
columns_mapping = {
    "annee": "Year",  # Année
    "patho_niv1": "Pathology Level 1",  # Pathologie niveau 1
    "patho_niv2": "Pathology Level 2",  # Pathologie niveau 2
    "patho_niv3": "Pathology Level 3",  # Pathologie niveau 3
    "top": "Topology",  # Topologie
    "cla_age_5": "Age Group (5 years)",  # Groupe d'âge (tranches de 5 ans)
    "sexe": "Gender",  # Sexe
    "region": "Region",  # Région
    "dept": "Department",  # Département
    "Ntop": "Patient Count (top)",  # Nombre de patients (topologie)
    "Npop": "Total Population",  # Population totale
    "prev": "Prevalence",  # Prévalence
    "Niveau prioritaire": "Priority Level",  # Niveau de priorité
    "libelle_classe_age": "Age Group Label",  # Étiquette groupe d'âge
    "libelle_sexe": "Gender Label",  # Étiquette sexe
    "tri": "Sorting"  # Ordre de tri
}

# Appliquer le renommage des colonnes au DataFrame
raw_file.rename(columns=columns_mapping, inplace=True)

# Écriture des données transformées dans un fichier de staging
try:
    raw_file.to_csv(staged_file_path, sep=",", index=False, encoding="utf-8-sig")
    print(f"Data successfully written to: {staged_file_path}")
except Exception as e:
    print(f"Error writing staged file: {e}")
    exit(1)
