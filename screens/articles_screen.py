from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from database.init_db import get_connection

ADMIN_PASSWORD = "1234"

class ArticlesScreen(Screen):
    rv_articles = ObjectProperty(None)
    articles = []

    def on_pre_enter(self):
        self.load_articles()

    def get_db(self):
        app = App.get_running_app()
        return get_connection(app.db_path)

    def load_articles(self):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles")
        rows = cur.fetchall()
        conn.close()
        self.articles = rows
        items = [
            f"{r['id']}: {r['nom']} - Stock {r['stock']} - Prix gros {r['prix_gros']} - Prix détail {r['prix_detail']}"
            for r in rows
        ]
        if self.rv_articles:
            self.rv_articles.data = [{"text": it, "selected": False} for it in items]

    # ---------- Ajout ----------
    def show_add_dialog(self):
        content = BoxLayout(orientation="vertical", spacing=6, padding=6)
        name = TextInput(hint_text="Nom")
        price_g = TextInput(hint_text="Prix gros")
        price_d = TextInput(hint_text="Prix détail")
        stock = TextInput(hint_text="Stock")
        qty_detail = TextInput(hint_text="Quantité par gros", text="1")
        content.add_widget(name)
        content.add_widget(price_g)
        content.add_widget(price_d)
        content.add_widget(stock)
        content.add_widget(qty_detail)

        btns = BoxLayout(size_hint_y=None, height="40dp", spacing=6)
        popup = Popup(title="Ajouter article", content=content, size_hint=(.9, .9))

        def add_article():
            try:
                conn = self.get_db()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO articles (nom, prix_gros, prix_detail, stock, quantite_detail) VALUES (?, ?, ?, ?, ?)",
                    (name.text, float(price_g.text), float(price_d.text), int(stock.text), int(qty_detail.text))
                )
                conn.commit()
                conn.close()
                popup.dismiss()
                self.load_articles()
            except Exception as e:
                self.show_message(f"Erreur ajout article: {e}")

        btns.add_widget(Button(text="OK", on_release=lambda *_: add_article()))
        btns.add_widget(Button(text="Annuler", on_release=lambda *_: popup.dismiss()))
        content.add_widget(btns)
        popup.open()

    # ---------- Modification ----------
    def show_edit_dialog(self):
        article = self.get_selected_article()
        if not article:
            self.show_message("Veuillez sélectionner un article pour modifier.")
            return

        if not self.ask_admin_password():
            return

        content = BoxLayout(orientation="vertical", spacing=6, padding=6)
        name = TextInput(text=article['nom'])
        price_g = TextInput(text=str(article['prix_gros']))
        price_d = TextInput(text=str(article['prix_detail']))
        stock = TextInput(text=str(article['stock']))
        qty_detail = TextInput(text=str(article['quantite_detail']))
        content.add_widget(name)
        content.add_widget(price_g)
        content.add_widget(price_d)
        content.add_widget(stock)
        content.add_widget(qty_detail)

        btns = BoxLayout(size_hint_y=None, height="40dp", spacing=6)
        popup = Popup(title="Modifier article", content=content, size_hint=(.9, .9))

        def save_changes():
            try:
                conn = self.get_db()
                cur = conn.cursor()
                cur.execute(
                    "UPDATE articles SET nom=?, prix_gros=?, prix_detail=?, stock=?, quantite_detail=? WHERE id=?",
                    (name.text, float(price_g.text), float(price_d.text), int(stock.text), int(qty_detail.text), article['id'])
                )
                conn.commit()
                conn.close()
                popup.dismiss()
                self.load_articles()
            except Exception as e:
                self.show_message(f"Erreur modification article: {e}")

        btns.add_widget(Button(text="Enregistrer", on_release=lambda *_: save_changes()))
        btns.add_widget(Button(text="Annuler", on_release=lambda *_: popup.dismiss()))
        content.add_widget(btns)
        popup.open()

    # ---------- Suppression ----------
    def delete_selected(self):
        article = self.get_selected_article()
        if not article:
            self.show_message("Veuillez sélectionner un article pour supprimer.")
            return

        if not self.ask_admin_password():
            return

        conn = self.get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM articles WHERE id=?", (article['id'],))
        conn.commit()
        conn.close()
        self.load_articles()

    # ---------- Helpers ----------
    def get_selected_article(self):
        if self.rv_articles and self.rv_articles.data:
            selected_text = self.rv_articles.data[0]['text']
            article_id = int(selected_text.split(":")[0])
            return next((a for a in self.articles if a['id'] == article_id), None)
        return None

    def show_message(self, message):
        popup = Popup(title="Info", content=Label(text=message), size_hint=(.6, .3))
        popup.open()

    def ask_admin_password(self):
        content = BoxLayout(orientation="vertical", spacing=6, padding=6)
        pwd_input = TextInput(password=True, multiline=False)
        content.add_widget(Label(text="Mot de passe admin :"))
        content.add_widget(pwd_input)
        btns = BoxLayout(size_hint_y=None, height="40dp", spacing=6)
        popup = Popup(title="Authentification", content=content, size_hint=(.8, .4))

        success = {'ok': False}

        def check_pwd():
            if pwd_input.text == ADMIN_PASSWORD:
                success['ok'] = True
                popup.dismiss()
            else:
                self.show_message("Mot de passe incorrect.")

        btns.add_widget(Button(text="OK", on_release=lambda *_: check_pwd()))
        btns.add_widget(Button(text="Annuler", on_release=lambda *_: popup.dismiss()))
        content.add_widget(btns)
        popup.open()
        popup.bind(on_dismiss=lambda *_: None)
        return success['ok']
