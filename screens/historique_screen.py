from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.recycleview import RecycleView
from database.init_db import get_connection
from utils.helpers import format_price

class HistoriqueScreen(Screen):
    rv_history = None

    def on_pre_enter(self):
        self.load_history()

    def get_db(self):
        app = App.get_running_app()
        return get_connection(app.db_path)

    def load_history(self):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("SELECT v.id, v.date, SUM(vi.quantite*vi.prix) as total "
                    "FROM ventes v "
                    "LEFT JOIN vente_items vi ON vi.vente_id=v.id "
                    "GROUP BY v.id, v.date "
                    "ORDER BY v.date DESC")
        rows = cur.fetchall()
        conn.close()

        items = [f"Vente {r['id']} - Date: {r['date']} - Total: {format_price(r['total'])}" for r in rows]

        if hasattr(self.ids, 'rv_history'):
            self.ids.rv_history.data = [{"text": it} for it in items]
