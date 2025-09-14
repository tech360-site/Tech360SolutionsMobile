from kivy.uix.screenmanager import Screen
from database.init_db import get_connection
from kivy.app import App
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from utils.helpers import format_price
import os

class RapportScreen(Screen):
    def get_db(self):
        app = App.get_running_app()
        return get_connection(app.db_path)

    def generate_report(self):
        start = self.ids.start_date.text
        end = self.ids.end_date.text
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT v.id, v.date, SUM(vi.quantite * vi.prix) AS total
            FROM ventes v
            LEFT JOIN vente_items vi ON vi.vente_id = v.id
            WHERE DATE(v.date) BETWEEN ? AND ?
            GROUP BY v.id
        """, (start, end))
        rows = cur.fetchall()
        conn.close()
        text = "\n".join([f"V{r['id']} {r['date']} {format_price(r['total'])} FCFA" for r in rows])
        popup = Popup(title="Rapport généré", content=BoxLayout(orientation='vertical'), size_hint=(.8,.8))
        popup.content.add_widget(Button(text=text, size_hint_y=None, height=200))
        popup.content.add_widget(Button(text="Fermer", size_hint_y=None, height=50, on_release=lambda *_: popup.dismiss()))
        popup.open()

    def export_pdf(self):
        app = App.get_running_app()
        out = os.path.join(app.user_data_dir, f"rapport_{self.ids.start_date.text}_{self.ids.end_date.text}.pdf")
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT v.id, v.date, SUM(vi.quantite * vi.prix) AS total
            FROM ventes v
            LEFT JOIN vente_items vi ON vi.vente_id = v.id
            WHERE DATE(v.date) BETWEEN ? AND ?
            GROUP BY v.id
        """, (self.ids.start_date.text, self.ids.end_date.text))
        rows = cur.fetchall()
        conn.close()
        c = canvas.Canvas(out, pagesize=A4)
        y = 800
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, y, f"Rapport {self.ids.start_date.text} → {self.ids.end_date.text}")
        y -= 30
        c.setFont("Helvetica", 12)
        total_global = 0
        for r in rows:
            c.drawString(40, y, f"V{r['id']} {r['date']} : {format_price(r['total'])} FCFA")
            y -= 18
            total_global += r['total'] or 0
            if y < 60:
                c.showPage(); y = 800
        c.drawString(40, y-20, f"Total global: {format_price(total_global)} FCFA")
        c.save()
        popup = Popup(title="Export PDF", content=BoxLayout(orientation='vertical'), size_hint=(.8,.8))
        popup.content.add_widget(Button(text=f"Fichier créé: {out}", size_hint_y=None, height=50))
        popup.content.add_widget(Button(text="Fermer", size_hint_y=None, height=50, on_release=lambda *_: popup.dismiss()))
        popup.open()
