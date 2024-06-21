from dotenv import load_dotenv
import os

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()
TOKEN = os.getenv('TOKEN')
LINKER = "./resources/linker.txt"
PERSO = "./resources/characters"