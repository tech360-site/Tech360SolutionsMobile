# database/init_db.py
import sqlite3
import os

def get_connection(db_path):
    """Retourne une connexion SQLite avec row_factory pour accéder par nom de colonne"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path):
    """Crée la base si absente et initialise toutes les tables"""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    if os.path.exists(db_path):
        print("Base existante :", db_path)
        return

    conn = get_connection(db_path)
    cur = conn.cursor()

    # Table articles
    cur.execute("""
        CREATE TABLE articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prix_gros REAL NOT NULL,
            prix_detail REAL NOT NULL,
            stock INTEGER NOT NULL,
            quantite_detail INTEGER NOT NULL DEFAULT 1
        )
    """)

    # Table ventes
    cur.execute("""
        CREATE TABLE ventes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL
        )
    """)

    # Table items de vente
    cur.execute("""
        CREATE TABLE vente_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vente_id INTEGER NOT NULL,
            article_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            quantite INTEGER NOT NULL,
            prix REAL NOT NULL,
            FOREIGN KEY(vente_id) REFERENCES ventes(id),
            FOREIGN KEY(article_id) REFERENCES articles(id)
        )
    """)

    # Table paramètres
    cur.execute("""
        CREATE TABLE IF NOT EXISTS parametres (
            cle TEXT PRIMARY KEY,
            valeur TEXT
        )
    """)

    # Valeurs par défaut
    default_params = [
        ("societe", "MiniSupermarché POS"),
        ("footer", "Merci pour votre achat !"),
        ("logo", ""),
        ("ticket_format", "80")
    ]
    for cle, valeur in default_params:
        cur.execute("INSERT OR IGNORE INTO parametres (cle, valeur) VALUES (?, ?)", (cle, valeur))

    conn.commit()
    conn.close()
    print("DB initialisée :", db_path)
