# utils/helpers.py
import json
from datetime import datetime
import os
from database.init_db import get_connection

PARAM_FILE_NAME = "params.json"

def current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_price(price):
    try:
        return f"{float(price):,.2f}"
    except:
        return str(price)

def load_params_from_db(db_path):
    conn = get_connection(db_path)
    cur = conn.cursor()
    try:
        cur.execute("SELECT cle, valeur FROM parametres")
        rows = cur.fetchall()
        params = {r["cle"]: r["valeur"] for r in rows}
    except Exception:
        params = {}
    finally:
        conn.close()
    # valeurs par défaut
    return {
        "societe": params.get("societe", "MiniSupermarché POS"),
        "footer": params.get("footer", "Merci pour votre achat !"),
        "logo": params.get("logo", ""),
        "ticket_format": params.get("ticket_format", "80")
    }

def save_param_to_db(db_path, key, value):
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO parametres (cle, valeur) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()
