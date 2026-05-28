"""
Point d'entrée principal de l'application ScootCheck.
Initialise et lance l'interface graphique.
"""

from gui import ScootCheckApp

def main():
    app = ScootCheckApp()
    app.mainloop()

if __name__ == "__main__":
    main()