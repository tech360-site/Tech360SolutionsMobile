from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
import os

from database.init_db import init_db
from utils.helpers import load_params_from_db, save_param_to_db

# screens imports
from screens.articles_screen import ArticlesScreen
from screens.ventes_screen import VentesScreen
from screens.caisse_screen import CaisseScreen
from screens.param_screen import ParamScreen
from screens.inventaire_screen import InventaireScreen
from screens.historique_screen import HistoriqueScreen
from screens.rapport_screen import RapportScreen

KV_FILE = os.path.join(os.path.dirname(__file__), "tech360.kv")

class MainApp(App):
    def build(self):
        # Créer le dossier de l'app pour DB et fichiers
        self.app_folder = self.user_data_dir
        os.makedirs(self.app_folder, exist_ok=True)
        self.db_path = os.path.join(self.app_folder, "minisupermarche.db")
        init_db(self.db_path)

        # Charger les paramètres
        self.params = load_params_from_db(self.db_path)

        Builder.load_file(KV_FILE)
        sm = ScreenManager()
        sm.add_widget(ArticlesScreen(name="articles"))
        sm.add_widget(VentesScreen(name="ventes"))
        sm.add_widget(CaisseScreen(name="caisse"))
        sm.add_widget(ParamScreen(name="param"))
        sm.add_widget(InventaireScreen(name="inventaire"))
        sm.add_widget(HistoriqueScreen(name="historique"))
        sm.add_widget(RapportScreen(name="rapport"))
        return sm

if __name__ == "__main__":
    MainApp().run()
