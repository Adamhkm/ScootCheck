def evaluate_maintenance(current_km, intervals):
    """
    Compare le kilométrage actuel avec les intervalles du JSON.
    Retourne un dictionnaire avec le statut de chaque pièce.
    """
    results = {}
    
    for part, interval in intervals.items():
        # Le modulo donne les km parcourus depuis le dernier entretien "théorique"
        km_since_last_check = current_km % interval 
        km_remaining = interval - km_since_last_check
        
        # On calcule un pourcentage d'usure (0.0 = neuf, 1.0 = entretien à faire)
        wear_ratio = km_since_last_check / interval
        
        # On définit les seuils d'alerte
        if wear_ratio >= 0.90 or km_remaining <= 15:
            status = "🔴 URGENT"
        elif wear_ratio >= 0.75:
            status = "🟠 À PRÉVOIR"
        else:
            status = "🟢 OK"
            
        results[part] = {
            "interval": interval,
            "km_remaining": km_remaining,
            "status": status
        }
        
    return results