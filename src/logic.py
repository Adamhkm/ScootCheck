def evaluate_maintenance(current_km, intervals, history=None):
    """
    Compare le kilométrage actuel avec le kilométrage du dernier entretien (historique).
    """
    if history is None:
        history = {}

    results = {}
    
    for part, interval in intervals.items():
        # Si on n'a pas d'historique, on suppose que le dernier entretien était au km 0
        last_checked_km = history.get(part, 0)
        
        # Le vrai calcul : combien de km parcourus depuis la dernière réparation ?
        km_since_last_check = current_km - last_checked_km
        
        # On évite les bugs si l'utilisateur tape un kilométrage inférieur à l'historique
        if km_since_last_check < 0:
            km_since_last_check = 0
            
        km_remaining = interval - km_since_last_check
        
        # Les alertes
        if km_since_last_check >= interval or km_remaining <= 15:
            status = "🔴 URGENT"
            km_remaining = 0 # On bloque à 0 pour que ce soit plus joli
        elif (km_since_last_check / interval) >= 0.75:
            status = "🟠 À PRÉVOIR"
        else:
            status = "🟢 OK"
            
        results[part] = {
            "interval": interval,
            "km_remaining": km_remaining,
            "status": status,
            "last_checked_km": last_checked_km
        }
        
    return results