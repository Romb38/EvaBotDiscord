from dotenv import load_dotenv
import os

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()
TOKEN = os.getenv('TOKEN')
LINKER = "./ressources/linker.txt"
PERSO = "./ressources/characters/"
HELP_LINK = "https://github.com/Romb38/EvaBotDiscord"