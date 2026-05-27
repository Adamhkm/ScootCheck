import customtkinter as ctk
from parser import list_available_scooters, load_scooter_data

# On configure le look (Dark mode et thème bleu)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ScootCheckApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        self.title("ScootCheck - Maintenance Hub")
        self.geometry("800x500")

        # --- Layout ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Sidebar (Menu de gauche)
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="🛴 ScootCheck", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # 2. Sélection du modèle
        self.label_model = ctk.CTkLabel(self.sidebar, text="Choose your model:", anchor="w")
        self.label_model.grid(row=1, column=0, padx=20, pady=(10, 0))
        
        scooters = list_available_scooters()
        self.option_menu = ctk.CTkOptionMenu(self.sidebar, values=scooters, command=self.on_scooter_change)
        self.option_menu.grid(row=2, column=0, padx=20, pady=10)

        # 3. Zone principale (Contenu)
        self.main_content = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.main_content.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.welcome_label = ctk.CTkLabel(self.main_content, text="Welcome to ScootCheck", font=ctk.CTkFont(size=24))
        self.welcome_label.pack(pady=20)
        
        self.status_label = ctk.CTkLabel(self.main_content, text="Please select a scooter and enter your mileage.")
        self.status_label.pack(pady=10)

    def on_scooter_change(self, choice):
        print(f"Modèle sélectionné : {choice}")
        self.status_label.configure(text=f"Model {choice} loaded. Ready for check.")

if __name__ == "__main__":
    app = ScootCheckApp()
    app.mainloop()