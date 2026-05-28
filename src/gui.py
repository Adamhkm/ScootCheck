"""
Interface Graphique Utilisateur (GUI).
Gère les interactions, l'affichage dynamique et la data-visualisation.
"""

import customtkinter as ctk
import tkinter.messagebox as messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from parser import list_available_scooters, load_scooter_data, load_history, save_history, add_expense, export_to_csv
from logic import evaluate_maintenance

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ScootCheckApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ScootCheck - Maintenance Hub")
        self.geometry("850x600")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_scooter_data = None
        self.current_scooter_filename = "" 

        self._build_sidebar()
        self._build_main_content()

    def _build_sidebar(self):
        """Construction du panneau latéral gauche."""
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="🛴 ScootCheck", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.label_model = ctk.CTkLabel(self.sidebar, text="Sélection du modèle:", anchor="w")
        self.label_model.grid(row=1, column=0, padx=20, pady=(10, 0))
        
        scooters = list_available_scooters()
        self.option_menu = ctk.CTkOptionMenu(self.sidebar, values=scooters, command=self.on_scooter_change)
        self.option_menu.grid(row=2, column=0, padx=20, pady=10)

    def _build_main_content(self):
        """Construction de la zone principale et des outils de contrôle."""
        self.main_content = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.header_label = ctk.CTkLabel(self.main_content, text="Tableau de bord", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.pack(pady=(0, 20))

        # --- Entrée utilisateur ---
        self.input_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.input_frame.pack(fill="x", pady=10)

        self.km_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Kilométrage actuel (km)", width=250)
        self.km_entry.pack(side="left", padx=(0, 10))
        self.km_entry.bind("<Return>", lambda event: self.run_check())

        self.check_button = ctk.CTkButton(self.input_frame, text="Analyser", command=self.run_check)
        self.check_button.pack(side="left")

        # --- Panneau financier et analytique ---
        self.stats_frame = ctk.CTkFrame(self.main_content, fg_color="#1f538d", corner_radius=10)
        self.stats_frame.pack(fill="x", pady=15, ipady=10)
        
        self.total_cost_lbl = ctk.CTkLabel(self.stats_frame, text="Dépenses: 0.00 €", font=ctk.CTkFont(size=15, weight="bold"))
        self.total_cost_lbl.pack(side="left", padx=15)
        
        self.add_expense_btn = ctk.CTkButton(self.stats_frame, text="➕ Ajout", width=80, fg_color="#2fa572", hover_color="#1e7b52", command=self.add_custom_expense)
        self.add_expense_btn.pack(side="left", padx=5)

        self.export_btn = ctk.CTkButton(self.stats_frame, text="📄 CSV", width=80, fg_color="#d4a017", hover_color="#b08513", command=self.export_data)
        self.export_btn.pack(side="left", padx=5)

        self.analytics_btn = ctk.CTkButton(self.stats_frame, text="📊 Graph", width=80, fg_color="#8e44ad", hover_color="#732d91", command=self.show_analytics)
        self.analytics_btn.pack(side="left", padx=5)

        self.cost_per_km_lbl = ctk.CTkLabel(self.stats_frame, text="Coût / km: 0.00 €", font=ctk.CTkFont(size=15, weight="bold"))
        self.cost_per_km_lbl.pack(side="right", padx=15)

        # --- Zone d'affichage des listes d'entretien ---
        self.result_frame = ctk.CTkScrollableFrame(self.main_content, width=500, height=250, fg_color="#2b2b2b")
        self.result_frame.pack(fill="both", expand=True)

        scooters = list_available_scooters()
        if scooters:
            self.on_scooter_change(scooters[0])

    def on_scooter_change(self, choice):
        """Gère le basculement entre différents modèles de trottinettes."""
        self.current_scooter_filename = choice
        self.current_scooter_data = load_scooter_data(choice)
        self.km_entry.delete(0, 'end')
        
        # Mise à jour de l'affichage financier initial
        history = load_history(choice)
        total_spent = history.get("total_spent", 0.0)
        self.total_cost_lbl.configure(text=f"Dépenses: {total_spent:.2f} €")
        self.cost_per_km_lbl.configure(text="Coût / km: En attente")
        
        for widget in self.result_frame.winfo_children():
            widget.destroy()

    def mark_as_done(self, part_key, current_km):
        """Valide une opération de maintenance et l'enregistre."""
        save_history(self.current_scooter_filename, part_key, current_km)
        
        prices = self.current_scooter_data.get("parts_average_price_eur", {})
        price = prices.get(part_key, 0.0)
        
        if price > 0:
            part_name = part_key.replace("_", " ").title()
            add_expense(self.current_scooter_filename, price, label=part_name)
            
        self.run_check()

    def run_check(self):
        """Déclenche l'algorithme d'analyse et met à jour l'interface visuelle."""
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        if not self.current_scooter_data:
            return

        try:
            km_text = self.km_entry.get().strip().replace(',', '.')
            km = float(km_text)
        except ValueError:
            error_lbl = ctk.CTkLabel(self.result_frame, text="❌ Erreur: Saisie invalide.", text_color="#ff4d4d")
            error_lbl.pack(pady=10)
            return

        history = load_history(self.current_scooter_filename)
        
        # Mise à jour des métriques financières
        total_spent = history.get("total_spent", 0.0)
        self.total_cost_lbl.configure(text=f"Dépenses: {total_spent:.2f} €")
        
        if km > 0:
            cost_per_km = total_spent / km
            self.cost_per_km_lbl.configure(text=f"Coût / km: {cost_per_km:.4f} €")

        intervals = self.current_scooter_data["maintenance_intervals_km"]
        analysis = evaluate_maintenance(km, intervals, history)

        for part, data in analysis.items():
            status = data["status"]
            remaining = data["km_remaining"]
            last_checked = data["last_checked_km"]
            part_name = part.replace("_", " ").title()

            if "URGENT" in status:
                color = "#ff4d4d"
            elif "PRÉVOIR" in status:
                color = "#ffa64d"
            else:
                color = "#4dff4d"

            item_frame = ctk.CTkFrame(self.result_frame, fg_color="#333333", corner_radius=8)
            item_frame.pack(fill="x", pady=5, padx=5)

            name_lbl = ctk.CTkLabel(item_frame, text=part_name, font=ctk.CTkFont(size=14, weight="bold"))
            name_lbl.pack(side="left", padx=15, pady=12)

            action_btn = ctk.CTkButton(item_frame, text="✔️ Fix", width=50, fg_color="#4d4d4d", hover_color="#5c5c5c",
                                       command=lambda p=part, k=km: self.mark_as_done(p, k))
            action_btn.pack(side="right", padx=10, pady=12)

            # L'affichage montre maintenant l'intelligence du système (mémoire)
            status_text = f"{status} (Reste: {remaining:.1f} km | Entretien à {last_checked} km)"
            status_lbl = ctk.CTkLabel(item_frame, text=status_text, text_color=color, font=ctk.CTkFont(size=13, weight="bold"))
            status_lbl.pack(side="right", padx=15, pady=12)

    def add_custom_expense(self):
        """Affiche les boîtes de dialogue pour la saisie manuelle de dépenses."""
        if not self.current_scooter_data:
            return

        dialog_name = ctk.CTkInputDialog(text="Description de la dépense :", title="Nouvelle dépense")
        expense_name = dialog_name.get_input()
        if not expense_name:
            return

        dialog_price = ctk.CTkInputDialog(text=f"Montant pour '{expense_name}' (€) :", title="Montant")
        price_text = dialog_price.get_input()
        if not price_text:
            return

        try:
            price = float(price_text.replace(',', '.'))
            if price > 0:
                add_expense(self.current_scooter_filename, price, label=expense_name)
                self.run_check()
        except ValueError:
            pass

    def export_data(self):
        """Génère l'export CSV de l'historique."""
        if not self.current_scooter_data:
            return
        filepath = export_to_csv(self.current_scooter_filename)
        messagebox.showinfo("Export Réussi", f"Fichier généré :\n{filepath}")

    def show_analytics(self):
        """Génère et affiche le diagramme circulaire des dépenses."""
        if not self.current_scooter_data:
            return

        history = load_history(self.current_scooter_filename)
        expenses = history.get("custom_expenses", [])

        if not expenses:
            messagebox.showinfo("Information", "Données insuffisantes pour générer l'analyse.")
            return

        data_aggregated = {}
        for exp in expenses:
            label = exp["label"]
            data_aggregated[label] = data_aggregated.get(label, 0) + exp["amount"]

        labels = list(data_aggregated.keys())
        values = list(data_aggregated.values())

        analytics_window = ctk.CTkToplevel(self)
        analytics_window.title("Analytique")
        analytics_window.geometry("600x500")
        analytics_window.attributes("-topmost", True) 

        fig, ax = plt.subplots(figsize=(6, 5), facecolor='#2b2b2b')
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, 
               textprops={'color':"white", 'fontsize': 12, 'weight': 'bold'},
               colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0'])
               
        ax.set_title(f"Répartition financière - {self.current_scooter_data['model_name']}", color='white', fontsize=14, weight='bold')

        canvas = FigureCanvasTkAgg(fig, master=analytics_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)