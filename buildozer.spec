[app]
# Nom affiché sur l'application
title = Tech360 Solutions

# Nom du package (identifiant unique)
package.name = tech360solutions
package.domain = org.tech360

# Répertoire source (là où se trouve ton main.py)
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json

# Fichiers exclus (exemple : fichiers cache)
# source.exclude_exts = spec,pyc,pyo

# Icône et image de lancement
icon.filename = %(source.dir)s/assets/logo.png
presplash.filename = %(source.dir)s/assets/logo.png

# Version de l'application
version = 1.0

# Mode plein écran (0 = non, 1 = oui)
fullscreen = 0

# Orientation (portrait, landscape ou all)
orientation = portrait

# Permissions Android nécessaires
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, CAMERA

# Bibliothèques Python nécessaires
requirements = python3,kivy==2.1.0,kivymd,Pillow,qrcode,pyjnius,fpdf2

# NDK API minimum (21 recommandé)
android.minapi = 21

# API cible Android
android.api = 31

# SDK/NDK spécifiques (Buildozer va les télécharger)
android.ndk = 25b
android.sdk = 31
android.ndk_api = 21

# Architectures supportées
archs = arm64-v8a, armeabi-v7a

# Ajouter SQLite (utile si ton app stocke des données)
android.sqlite3 = True

# Application sera signée automatiquement avec une clé debug
android.release_artifact = apk


[buildozer]
# Niveau de log
log_level = 2

# Attention si root
warn_on_root = 1

# Répertoire où seront stockés les fichiers de compilation
build_dir = .buildozer
