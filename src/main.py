from parser import list_available_scooters, load_scooter_data

def main():
    print("--- 🛴 Bienvenue dans ScootCheck ---")
    
    # 1. On liste les fichiers disponibles
    files = list_available_scooters()
    print(f"\nFichiers trouvés dans la base de données : {files}")
    
    # 2. On fait un test avec la Kukirin
    test_file = "kukirin_g2_master.json"
    
    if test_file in files:
        print(f"\nTentative de chargement de {test_file}...")
        kukirin_data = load_scooter_data(test_file)
        
        if kukirin_data:
            # En Python, on accède aux valeurs d'un dictionnaire avec dict["cle"]
            nom_modele = kukirin_data["model_name"]
            pression_pneus = kukirin_data["maintenance_intervals_km"]["tire_pressure"]
            
            print(f"✅ Succès ! Modèle chargé : {nom_modele}")
            print(f"ℹ️  Info : La pression des pneus doit être vérifiée tous les {pression_pneus} km.")

if __name__ == "__main__":
    main()