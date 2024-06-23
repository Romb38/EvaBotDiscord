# E.V.A. Discord bot

Il s'agit d'un bot discord disponible pour le RP evaporate

# Author
Romb38

# Installation

Récuperez le token de votre bot discord sur le site de discord developper

Pour Debian/Ubuntu:
```bash
TOKEN=your_token
git clone https://github.com/Romb38/EvaBotDiscord.git
cd EvaBotDiscord
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "TOKEN=$TOKEN" > .env
python3 main.py
```

Pour Windows:
```bash
set TOKEN=your_token
git clone https://github.com/Romb38/EvaBotDiscord.git
cd EvaBotDiscord
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
echo "TOKEN=$TOKEN" > .env
python main.py
```

# Commands

Incarnation:
  add                 Ajoute une valeur aux statistiques
  connect             Lie un joueur à une incarnation en utilisant un slug.
  d                   Renvoie un nombre aléatoire entre 1 et le nombre spécifié
  d20                 Lance un dé à 20 faces
  d4                  Lance un dé à 4 faces
  d6                  Lance un dé à 6 faces
  disconnect          Dé-lie un joueur et son incarnation
  plist               Liste les incarnations et leurs joueurs
MJ:
  add_insanite        Ajoute de l'insanité à un personnage
  add_insanite_all    Ajoute de l'insanité à tous
  add_savoir          Ajoute un niveau à une compétence de quelqu'un
  ending              Nettoie les rôles et salons créés par la commande init.
  fdisconnect         Dé-lie de force un personnage et son incarnation
  init                Initialise les rôles et salons pour les personnages.
  lvlup               Ajoute un level à quelqu'un
  lvlup_all           Ajoute un level à toutes les incarnations
  ping                Vérifier si le bot fonctionne
  remove_insanite     Retire de l'insanité à un personnage
  remove_insanite_all Retire de l'insanité à tous
  show_stats          Affiche les stats d'un joueur
No Category:
  help                Shows this message

Type !help command for more info on a command.
You can also type !help category for more info on a category.
