from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from database.init_db import get_connection
from utils.helpers import load_params_from_db, save_param_to_db


class ParamScreen(Screen):
    logo_path = ""

    def on_pre_enter(self):
        """
        Charger les paramètres depuis la base lorsque l'écran est ouvert.
        """
        app = App.get_running_app()
        self.db_path = app.db_path
        params = load_params_from_db(self.db_path)

        self.ids.societe_input.text = params.get('societe', '')
        self.ids.footer_input.text = params.get('footer', '')
        self.logo_path = params.get('logo', '')
        self.ids.logo_preview.source = self.logo_path
        self.ids.format_spinner.text = params.get('ticket_format', '80')

    def save_params(self):
        """
        Sauvegarder les paramètres modifiés dans la base.
        """
        save_param_to_db(self.db_path, "societe", self.ids.societe_input.text)
        save_param_to_db(self.db_path, "footer", self.ids.footer_input.text)
        save_param_to_db(self.db_path, "logo", self.logo_path)
        save_param_to_db(self.db_path, "ticket_format", self.ids.format_spinner.text)

        # Affichage popup confirmation
        popup = Popup(
            title="Succès",
            content=Button(text="Paramètres enregistrés", on_release=lambda x: popup.dismiss()),
            size_hint=(0.5, 0.3)
        )
        popup.open()

    def choose_logo(self):
        """
        Ouvre un file chooser pour sélectionner l'image du logo.
        """
        box = BoxLayout(orientation='vertical', spacing=6)
        filechooser = FileChooserListView(filters=['*.png', '*.jpg', '*.jpeg'])
        box.add_widget(filechooser)

        btn = Button(text="Valider", size_hint_y=None, height=40)
        box.add_widget(btn)

        popup = Popup(title="Choisir logo", content=box, size_hint=(0.9, 0.9))

        def select_file(instance):
            if filechooser.selection:
                self.logo_path = filechooser.selection[0]
                self.ids.logo_preview.source = self.logo_path
                popup.dismiss()

        btn.bind(on_release=select_file)
        popup.open()
