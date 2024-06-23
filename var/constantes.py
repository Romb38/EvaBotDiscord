import asyncio

from dotenv import load_dotenv
import os
import platform

# Vérifiez si le système d'exploitation est Windows
if platform.system() == 'Windows':
    encoding = 'utf-16'
else:
    encoding = 'utf-8'

# Chargez les variables d'environnement avec l'encodage approprié
load_dotenv(encoding=encoding)

TOKEN = os.getenv('TOKEN')
LINKER = "./ressources/linker.txt"
PERSO = "./ressources/characters/"

LVL_UP_COMBAT_STAT=1
LVL_UP_HORS_COMBAT_STAT=2

semaphore = asyncio.Semaphore(1)

isHelp=False