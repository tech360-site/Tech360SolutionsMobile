from kivy.uix.screenmanager import Screen
from database.init_db import get_connection
from kivy.app import App
from utils.helpers import format_price

class InventaireScreen(Screen):
    def on_pre_enter(self):
        self.load_inventory()

    def get_db(self):
        app = App.get_running_app()
        return get_connection(app.db_path)

    def load_inventory(self):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles")
        rows = cur.fetchall()
        conn.close()
        items = [
            f"{r['id']}: {r['nom']} - Stock {r['stock']} - Prix gros: {format_price(r['prix_gros'])} - Prix détail: {format_price(r['prix_detail'])}"
            for r in rows
        ]
        self.ids.rv_inventory.data = [{"text": it} for it in items]
