from kivy.uix.screenmanager import Screen
from kivy.app import App
from database.init_db import get_connection
from utils.helpers import format_price
from kivy.clock import Clock

class CaisseScreen(Screen):
    def on_pre_enter(self):
        # Mettre à jour total automatiquement
        Clock.schedule_once(lambda dt: self.update_total())

    def get_db(self):
        app = App.get_running_app()
        return get_connection(app.db_path)

    def update_total(self):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT IFNULL(SUM(vi.quantite * vi.prix), 0) AS total
            FROM ventes v
            LEFT JOIN vente_items vi ON vi.vente_id = v.id
            WHERE DATE(v.date) = DATE('now')
        """)
        total = cur.fetchone()["total"]
        conn.close()
        self.ids.caisse_total.text = f"Total du jour : {format_price(total)} FCFA"
        # Ajouter aperçu ticket
        cur = self.get_db().cursor()
        cur.execute("""
            SELECT vi.quantite, a.nom, vi.prix
            FROM vente_items vi
            JOIN articles a ON a.id = vi.article_id
            JOIN ventes v ON v.id = vi.vente_id
            WHERE DATE(v.date) = DATE('now')
        """)
        rows = cur.fetchall()
        ticket = "\n".join([f"{r['quantite']} x {r['nom']} = {format_price(r['prix']*r['quantite'])} FCFA" for r in rows])
        self.ids.ticket_preview.text = ticket if ticket else "Aucune vente aujourd'hui"
