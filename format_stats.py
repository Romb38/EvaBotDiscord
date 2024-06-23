import json
import os

import discord


def aff_stat(file):
    with open(file, 'r') as json_file:
        data = json.load(json_file)

    embed = discord.Embed(title=f"Statistiques de {data['nom']} {data['prenom']} ( lvl {data['level']} )", color=0x00ff00)

    # Ajouter les statistiques de combat
    combat_stats = format_combat_stats(data['stats']['combat'])
    embed.add_field(name="Combat", value=combat_stats, inline=True)

    # Ajouter les statistiques hors combat
    hors_combat_stats = format_hors_combat_stats(data['stats']['hors_combat'])
    embed.add_field(name="Hors-combat", value=hors_combat_stats, inline=True)

    # Ajouter les autres statistiques
    other_stats = format_other_stats(data['stats'], data["combat_left_to_attribute"], data["hors_left_to_attribute"])
    embed.add_field(name="Autres", value=other_stats, inline=True)

    # Ajouter un séparateur
    embed.add_field(name="\u200B", value="\u200B", inline=False)

    # Ajouter les compétences
    competences = format_competences(data['competence'])
    embed.add_field(name="Compétences", value=competences, inline=True)

    # Ajouter les savoirs
    savoirs = format_savoirs(data['savoir'])
    embed.add_field(name="Savoirs", value=savoirs, inline=True)

    return embed


def format_combat_stats(combat_stats):
    stats = "\n".join([f"| {key.capitalize()} : {value}" for key, value in combat_stats.items()])
    return stats

def format_hors_combat_stats(hors_combat_stats):
    stats = "\n".join([f"| {key.capitalize()} : {value}" for key, value in hors_combat_stats.items()])
    return stats

def format_other_stats(stats,cb,hc):
    other_stats = f"| Insanité : {stats['insanite']}\n"
    other_stats += f"| Initiative : {stats['initiative']}\n"
    other_stats += f"| Chance : {stats['chance']}\n"
    other_stats += f"| Restant combat : {cb}\n"
    other_stats += f"| Restant hors-combat : {hc}"
    return other_stats

def format_competences(competences):
    if not competences:
        return "Aucune compétence"
    formatted = "\n".join([f"{comp['title']} (Niveau {comp['lvl']})" for comp in competences if comp['lvl'] != 0])
    if formatted.replace("\n","").strip() == "":
        return "Aucune compétence"
    return formatted

def format_savoirs(savoirs):
    if not savoirs:
        return "Aucun savoir"
    formatted = "\n".join([f"{savoir['title']} (Niveau {savoir['lvl']})" for savoir in savoirs if savoir['lvl'] != 0])
    if formatted.replace("\n","").strip() == "":
        return "Aucun savoir"
    return formatted

async def update_character_stats_message(bot, json_file_path):
    # Lire le fichier JSON
    if not os.path.exists(json_file_path):
        print(f"Le fichier {json_file_path} n'existe pas.")
        return

    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    channel_id = data['admin'].get('channel')
    last_msg_id = data['admin'].get('last-msg')

    # Vérifier si l'ID du canal existe
    if not channel_id:
        print("L'ID du canal est manquant.")
        return

    channel = bot.get_channel(int(channel_id))
    if not channel:
        print(f"Le canal avec l'ID {channel_id} n'a pas été trouvé.")
        return

    # Supprimer le dernier message
    if last_msg_id:
        try:
            last_msg = await channel.fetch_message(int(last_msg_id))
            await last_msg.delete()
        except discord.NotFound:
            print(f"Le message avec l'ID {last_msg_id} n'a pas été trouvé.")
        except discord.Forbidden:
            print(f"Permission refusée pour supprimer le message avec l'ID {last_msg_id}.")
        except discord.HTTPException as e:
            print(f"Erreur HTTP lors de la suppression du message: {e}")

    embed = aff_stat(json_file_path)
    stats_message = await channel.send(embed=embed)

    # Mettre à jour l'ID du dernier message dans le fichier JSON
    data['admin']['last-msg'] = stats_message.id
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Les statistiques ont été envoyées et l'ID du dernier message a été mis à jour.")