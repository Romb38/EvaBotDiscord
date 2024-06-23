import asyncio

from dotenv import load_dotenv
import os

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()
TOKEN = os.getenv('TOKEN')
LINKER = "./ressources/linker.txt"
PERSO = "./ressources/characters/"

LVL_UP_COMBAT_STAT=1
LVL_UP_HORS_COMBAT_STAT=2

semaphore = asyncio.Semaphore(1)