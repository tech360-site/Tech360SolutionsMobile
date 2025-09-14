from kivy.uix.screenmanager import Screen
from kivy.app import App
from database.init_db import get_connection
from utils.helpers import format_price, current_datetime
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class VentesScreen(Screen):

    def on_pre_enter(self):
        self.load_articles()
        if not hasattr(self, 'cart'):
            self.cart = []

    def get_db(self):
        app = App.get_running_app()
        return get_connection(app.db_path)

    def load_articles(self):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles")
        self.articles = cur.fetchall()
        conn.close()
        self.filter_articles(self.ids.search_input.text if hasattr(self.ids, 'search_input') else "")

    def filter_articles(self, text):
        txt = text.lower()
        items = [f"{a['id']}: {a['nom']} - Stock {a['stock']} - Prix gros {a['prix_gros']}" for a in self.articles if txt in a['nom'].lower()]
        self.ids.rv_articles_v.data = [{"text": it} for it in items]

    def add_to_cart(self):
        search = self.ids.search_input.text.lower()
        article = next((a for a in self.articles if search in a['nom'].lower()), None)
        if not article and self.articles:
            article = self.articles[0]
        if not article:
            return
        try:
            qty = int(self.ids.qty_input.text)
        except:
            qty = 1
        sale_type = self.ids.type_spinner.text
        price = article['prix_gros'] if sale_type=="gros" else article['prix_detail']
        # vérifier si déjà dans le panier
        existing = next((i for i in self.cart if i['id']==article['id']), None)
        if existing:
            existing['qty'] += qty
        else:
            self.cart.append({"id": article['id'], "nom": article['nom'], "qty": qty, "prix": price, "type": sale_type})
        self.update_cart_label()

    def update_cart_label(self):
        total = sum(item['qty']*item['prix'] for item in self.cart)
        lines = [f"{i['nom']} x {i['qty']} = {format_price(i['qty']*i['prix'])}" for i in self.cart]
        self.ids.cart_label.text = "\n".join(lines) + f"\nTotal: {format_price(total)}"

    def remove_from_cart(self, article_id):
        self.cart = [i for i in self.cart if i['id'] != article_id]
        self.update_cart_label()

    def modify_quantity(self, article_id, new_qty):
        for i in self.cart:
            if i['id']==article_id:
                i['qty'] = new_qty
        self.update_cart_label()

    def validate_sale(self):
        if not self.cart:
            return
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO ventes (date) VALUES (?)", (current_datetime(),))
        vente_id = cur.lastrowid
        for item in self.cart:
            cur.execute("INSERT INTO vente_items (vente_id, article_id, type, quantite, prix) VALUES (?, ?, ?, ?, ?)",
                        (vente_id, item['id'], item['type'], item['qty'], item['prix']))
            cur.execute("UPDATE articles SET stock = stock - ? WHERE id=?", (item['qty'], item['id']))
        conn.commit()
        conn.close()
        self.cart = []
        self.update_cart_label()
        self.load_articles()
