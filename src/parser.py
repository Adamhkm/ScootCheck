"""
Module de gestion des données (Parser).
Gère la lecture des JSON, l'écriture des historiques et l'export CSV.
"""

import json
import os
import csv

DATA_DIR = "data"

def list_available_scooters():
    """Retourne la liste des modèles de trottinettes disponibles dans la base de données."""
    scooters = []
    if not os.path.exists(DATA_DIR):
        return scooters
        
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json") and not filename.endswith("_history.json"):
            scooters.append(filename)
    return scooters

def load_scooter_data(filename):
    """Charge les données techniques d'un modèle spécifique."""
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def get_history_filepath(filename):
    """Génère le chemin d'accès au fichier d'historique de maintenance."""
    base_name = filename.replace(".json", "")
    return os.path.join(DATA_DIR, f"{base_name}_history.json")

def load_history(filename):
    """Charge l'historique d'entretien et les dépenses associées."""
    filepath = get_history_filepath(filename)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
    return {}

def save_history(filename, part_key, current_km):
    """Enregistre le kilométrage lors d'une intervention sur une pièce."""
    history = load_history(filename)
    history[part_key] = current_km
    
    filepath = get_history_filepath(filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(history, file, indent=4)

def add_expense(filename, amount, label=None):
    """Ajoute une dépense financière à l'historique global."""
    history = load_history(filename)
    
    current_total = history.get("total_spent", 0.0)
    history["total_spent"] = current_total + amount
    
    if label:
        if "custom_expenses" not in history:
            history["custom_expenses"] = []
        history["custom_expenses"].append({"label": label, "amount": amount})
        
    filepath = get_history_filepath(filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(history, file, indent=4)

def export_to_csv(filename):
    """Génère un rapport d'export complet au format CSV."""
    history = load_history(filename)
    base_name = filename.replace(".json", "")
    export_path = f"{base_name}_export.csv"
    
    with open(export_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Categorie", "Element", "Valeur"])
        
        for key, value in history.items():
            if key not in ["total_spent", "custom_expenses"]:
                nom_propre = key.replace("_", " ").title()
                writer.writerow(["Entretien", nom_propre, f"{value} km"])
                
        for exp in history.get("custom_expenses", []):
            writer.writerow(["Depense", exp["label"], f"{exp['amount']} EUR"])
            
        writer.writerow(["---", "---", "---"])
        writer.writerow(["Bilan", "Cout Total", f"{history.get('total_spent', 0.0)} EUR"])
        
    return export_path