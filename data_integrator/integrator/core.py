# import os
# import pandas as pd
# import datetime
# import gc
# import numpy as np

# # Répertoire contenant les fichiers raw
# current_year = datetime.datetime.now().year
# raw_files_dir = "../../archived/raw"
# staged_file_path = f"../../archived/staged/staged_data_{current_year}.csv"

# def get_latest_raw_file(directory):
#     try:
#         # Lister les fichiers qui commencent par "raw_data" et se terminent par ".csv"
#         files = [os.path.join(directory, f) for f in os.listdir(directory) if f.startswith("raw_data") and f.endswith(".csv")]
#         if not files:
#             raise FileNotFoundError("No raw_data files found in the directory.")
#         # Retourner le fichier avec la date de modification la plus récente
#         return max(files, key=os.path.getmtime)
#     except Exception as e:
#         raise Exception(f"Error finding latest raw file: {e}")

# try:
#     raw_file_path = get_latest_raw_file(raw_files_dir)
#     print(f"Latest raw file detected: {raw_file_path}")
# except Exception as e:
#     print(f"Error: {e}")
#     exit(1)

# # Lecture du fichier par chunksize (optimisation de la mémoire)
# chunk_size = 5000
# dtype_dict = {
#     "Year": str,  # Année sous forme de chaîne
#     "Pathology Level 1": str,  # Niveau 1 des pathologies
#     "Pathology Level 2": str,  # Niveau 2 des pathologies
#     "Pathology Level 3": str,  # Niveau 3 des pathologies
#     "Topology": str,  # Topologie
#     "Age Group (5 years)": str,  # Groupe d'âge (tranches de 5 ans)
#     "Gender": str,  # Sexe
#     "Region": str,  # Région géographique
#     "Department": str,  # Département géographique
#     "Patient Count (top)": int,  # Nombre de patients (topologie)
#     "Total Population": int,  # Population totale
#     "Prevalence": float,  # Prévalence sous forme flottante
#     "Priority Level": str,  # Niveau de priorité
#     "Age Group Label": str,  # Étiquette du groupe d'âge
#     "Gender Label": str,  # Étiquette du sexe
#     "Sorting": int  # Tri
# }

# print(f"Reading raw file from: {raw_file_path}")
# try:
#     chunks = []
#     # Lire le fichier par morceaux (chunks)
#     for chunk in pd.read_csv(raw_file_path, sep=";", header=0, skipinitialspace=True, encoding="utf-8", dtype=dtype_dict, chunksize=chunk_size):
#         chunks.append(chunk)
#         del chunk
#         gc.collect()
#     # Concaténer les morceaux pour former un DataFrame complet
#     raw_file = pd.concat(chunks)
# except Exception as e:
#     print(f"Error reading raw file: {e}")
#     exit(1)

# # Renommage des colonnes
# columns_mapping = {
#     "annee": "Year",  # Année
#     "patho_niv1": "Pathology Level 1",  # Pathologie niveau 1
#     "patho_niv2": "Pathology Level 2",  # Pathologie niveau 2
#     "patho_niv3": "Pathology Level 3",  # Pathologie niveau 3
#     "top": "Topology",  # Topologie
#     "cla_age_5": "Age Group (5 years)",  # Groupe d'âge (tranches de 5 ans)
#     "sexe": "Gender",  # Sexe
#     "region": "Region",  # Région
#     "dept": "Department",  # Département
#     "Ntop": "Patient Count (top)",  # Nombre de patients (topologie)
#     "Npop": "Total Population",  # Population totale
#     "prev": "Prevalence",  # Prévalence
#     "Niveau prioritaire": "Priority Level",  # Niveau de priorité
#     "libelle_classe_age": "Age Group Label",  # Étiquette groupe d'âge
#     "libelle_sexe": "Gender Label",  # Étiquette sexe
#     "tri": "Sorting"  # Ordre de tri
# }

# # Appliquer le renommage des colonnes au DataFrame
# raw_file.rename(columns=columns_mapping, inplace=True)
# raw_file = raw_file.astype(str).fillna("")  # Chuyển mọi giá trị thành chuỗi và thay thế NaN bằng chuỗi rỗng

# # Écriture des données transformées dans un fichier de staging
# try:
#     raw_file.to_csv(staged_file_path, sep=",", index=False, encoding="utf-8-sig")
#     print(f"Data successfully written to: {staged_file_path}")
# except Exception as e:
#     print(f"Error writing staged file: {e}")
#     exit(1)

# del raw_file
# gc.collect()

import os
import pandas as pd
import datetime
import gc
import psutil

# Hàm theo dõi mức sử dụng bộ nhớ
def memory_usage():
    process = psutil.Process(os.getpid())
    return f"Memory Usage: {process.memory_info().rss / 1024 ** 2:.2f} MB"

# Đường dẫn và cấu hình
current_year = 2024
raw_files_dir = "../../archived/raw"
staged_file_path = f"../../archived/staged/staged_data_{current_year}.csv"
chunk_size = 5000  # Kích thước chunk tối ưu

columns_mapping = {
    "annee": "Year",
    "patho_niv1": "Pathology Level 1",
    "patho_niv2": "Pathology Level 2",
    "patho_niv3": "Pathology Level 3",
    "top": "Topology",
    "cla_age_5": "Age Group (5 years)",
    "sexe": "Gender",
    "region": "Region",
    "dept": "Department",
    "Ntop": "Patient Count (top)",
    "Npop": "Total Population",
    "prev": "Prevalence",
    "Niveau prioritaire": "Priority Level",
    "libelle_classe_age": "Age Group Label",
    "libelle_sexe": "Gender Label",
    "tri": "Sorting"
}

dtype_dict = {
    "Year": str,
    "Pathology Level 1": str,
    "Pathology Level 2": str,
    "Pathology Level 3": str,
    "Topology": str,
    "Age Group (5 years)": str,
    "Gender": str,
    "Region": str,
    "Department": str,
    "Patient Count (top)": int,
    "Total Population": int,
    "Prevalence": float,
    "Priority Level": str,
    "Age Group Label": str,
    "Gender Label": str,
    "Sorting": int
}

# Hàm tìm file mới nhất trong thư mục raw
def get_latest_raw_file(directory):
    try:
        # Obtenir l'année actuelle
        # Utilisation de la fonction datetime pour récupérer l'année au format AAAA
        current_year = datetime.now().strftime("%Y")
        
        # Récupérer tous les fichiers dans le répertoire correspondant au modèle "raw_data_$année.csv"
        # Les fichiers doivent commencer par "raw_data_année" et se terminer par ".csv"
        files = [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if f.startswith(f"raw_data_{current_year}") and f.endswith(".csv")
        ]
        
        # Si aucun fichier correspondant n'est trouvé, lever une exception
        if not files:
            raise FileNotFoundError(f"Aucun fichier raw_data pour l'année {current_year} trouvé dans le répertoire.")
        
        # Retourner le fichier le plus récent en fonction de sa date de modification
        return max(files, key=os.path.getmtime)
    
    except Exception as e:
        # Si une erreur survient, lever une exception avec un message détaillé
        raise Exception(f"Erreur lors de la recherche du dernier fichier raw : {e}")

# Lấy đường dẫn file raw mới nhất
try:
    raw_file_path = get_latest_raw_file(raw_files_dir)
    print(f"Latest raw file detected: {raw_file_path}")
except Exception as e:
    print(f"Error: {e}")
    exit(1)

# Đọc và xử lý dữ liệu từng chunk
print(f"Memory before processing: {memory_usage()}")
try:
    with open(staged_file_path, mode="w", encoding="utf-8-sig") as f_out:
        for i, chunk in enumerate(pd.read_csv(
            raw_file_path,
            sep=";",
            header=0,
            skipinitialspace=True,
            encoding="utf-8",
            dtype=dtype_dict,
            chunksize=chunk_size
        )):
            
            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1} chunks...")
                print(f"Memory after processing chunk {i + 1}: {memory_usage()}")

            # print(f"Processing chunk {i + 1}...")
            
            # Renommer les colonnes
            chunk.rename(columns=columns_mapping, inplace=True)

            # Convertir en chaîne et remplacer NaN
            chunk = chunk.astype(str).fillna("")

            # Écrire dans le fichier staging
            chunk.to_csv(f_out, sep=",", index=False, mode="a", header=(i == 0))
            
            # Libérer la mémoire
            del chunk
            gc.collect()

except Exception as e:
    print(f"Error processing raw file: {e}")
    exit(1)

print(f"Data successfully written to: {staged_file_path}")
print(f"Memory after completion: {memory_usage()}")
