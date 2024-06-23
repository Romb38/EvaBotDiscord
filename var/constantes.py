import asyncio

from dotenv import load_dotenv
import os
import platform

# Chargez les variables d'environnement avec l'encodage appropriée
try :
    load_dotenv(encoding="utf-8")
except Exception as e:
    load_dotenv(encoding="utf-16")


TOKEN = os.getenv('TOKEN')
LINKER = "./ressources/linker.txt"
PERSO = "./ressources/characters/"

LVL_UP_COMBAT_STAT=1
LVL_UP_HORS_COMBAT_STAT=2

semaphore = asyncio.Semaphore(1)

isHelp=False