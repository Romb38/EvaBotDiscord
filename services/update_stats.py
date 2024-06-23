import json
from var.constantes import *


def add_stats(file, stats, count):
    with open(file, 'r') as json_file:
        data = json.load(json_file)


    # Ajouter la valeur count au champ stats
    if stats in data["stats"]["combat"]:
        #Stats en combats
        point = data.get("combat_left_to_attribute")
        if point < count:
            return f"\u274C - Il ne vous reste que {point} points de statistiques à distribuer. Rien à été modifié"
        data["stats"]["combat"][stats] += count
        data["combat_left_to_attribute"] -= count
    elif stats in data["stats"]["hors_combat"]:
        # Stats hors combat
        point = data.get("hors_left_to_attribute")
        if point < count:
            return f"\u274C - Il ne vous reste que {point} points de statistiques à distribuer. Rien à été modifié"
        data["stats"]["hors_combat"][stats] += count
        data["hors_left_to_attribute"] -= count
    else:
        return "\u274C - Cette statistique n'existe pas"

    # Écrire les modifications dans le fichier
    with open(file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    return "\u2705 - Points attribués avec succès"


def add_insanite(file):
    with open(file, 'r') as json_file:
        data = json.load(json_file)

    data["stats"]["insanite"] += 1

    # Écrire les modifications dans le fichier
    with open(file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    return


def remove_insanite(file):
    with open(file, 'r') as json_file:
        data = json.load(json_file)

    data["stats"]["insanite"] -= 1

    # Écrire les modifications dans le fichier
    with open(file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    return


def lvl_up(file):
    with open(file, 'r') as json_file:
        data = json.load(json_file)

    data["level"] += 1
    data["combat_left_to_attribute"] += LVL_UP_COMBAT_STAT
    data["hors_left_to_attribute"] += LVL_UP_HORS_COMBAT_STAT

    # Écrire les modifications dans le fichier
    with open(file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    return

def add_competence(file, comp_name):
    with open(file, 'r') as json_file:
        data = json.load(json_file)

    # Chercher la compétence spécifiée
    competence_found = False
    for competence in data.get('competence', []):
        if competence['title'] == comp_name:
            competence_found = True
            if competence['lvl'] >= 6:
                return f"Erreur : Le niveau de la compétence '{comp_name}' est déjà au maximum (6)."
            else:
                competence['lvl'] += 1
                break

    if not competence_found:
        return f"Erreur : La compétence '{comp_name}' n'existe pas."

    # Enregistrer les modifications dans le fichier
    with open(file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    return f"Le niveau de la compétence '{comp_name}' a été augmenté de 1."

def add_savoir(file, savoir_name):
    with open(file, 'r') as json_file:
        data = json.load(json_file)

    # Chercher la compétence spécifiée
    competence_found = False
    for competence in data.get('savoir', []):
        if competence['title'] == savoir_name:
            competence_found = True
            if competence['lvl'] >= 6:
                return f"Erreur : Le niveau du savoir '{savoir_name}' est déjà au maximum (6)."
            else:
                competence['lvl'] += 1
                break

    if not competence_found:
        return f"Erreur : Le savoir '{savoir_name}' n'existe pas."

    # Enregistrer les modifications dans le fichier
    with open(file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    return f"Le niveau du savoir '{savoir_name}' a été augmenté de 1."
