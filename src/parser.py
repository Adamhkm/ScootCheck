import json
import os

# On définit le chemin vers le dossier qui contient les JSON
DATA_DIR = "data"

def list_available_scooters():
    """Parcourt le dossier data et retourne la liste des fichiers JSON."""
    scooters = []
    # On vérifie que le dossier existe bien
    if not os.path.exists(DATA_DIR):
        print(f"Erreur : Le dossier '{DATA_DIR}' est introuvable.")
        return scooters
        
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            scooters.append(filename)
    return scooters

def load_scooter_data(filename):
    """Ouvre un fichier JSON et le transforme en dictionnaire Python."""
    filepath = os.path.join(DATA_DIR, filename)
    
    try:
        # On ouvre le fichier en mode lecture ('r')
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file) # La magie opère ici : JSON -> Dict Python
            return data
    except FileNotFoundError:
        print(f"Erreur : Le fichier {filepath} n'existe pas.")
        return None
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier {filepath} est mal formaté.")
        return None