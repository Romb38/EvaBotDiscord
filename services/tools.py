import discord

from var.constantes import *


def update_linker_file(slug, player_pseudo, directory=PERSO, linker_file=LINKER, ):
    # Lire le contenu actuel de linker.txt s'il existe
    if os.path.exists(linker_file):
        with open(linker_file, 'r') as f:
            existing_entries = f.read().splitlines()
    else:
        existing_entries = []

    # Vérifier si le slug correspond à un fichier existant
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    slugs = [f.replace('.json', '') for f in json_files]

    if slug not in slugs:
        return "error_slug_not_found"

    # Vérifier si le slug est déjà pris
    for entry in existing_entries:
        if entry.startswith(slug + ':'):
            if player_pseudo in entry:
                return "error_pseudo_already_taken"

            # Mettre à jour l'entrée existante avec le nouveau pseudo
            existing_entries[existing_entries.index(entry)] = entry + ' ' + player_pseudo

            # Écrire les entrées mises à jour dans linker.txt
            with open(linker_file, 'w') as f:
                f.write('\n'.join(existing_entries) + '\n')
            return "success"

    # Ajouter une nouvelle entrée si le slug n'est pas trouvé
    new_entry = f"{slug}: {player_pseudo}"
    existing_entries.append(new_entry)
    with open(linker_file, 'a') as f:
        f.write(new_entry + '\n')

    return "success"


def create_or_update_linker_file(directory=PERSO, linker_file=LINKER):
    # Get list of files in the directory
    files_in_directory = os.listdir(directory)
    # Remove extensions from files
    files_without_extension = [os.path.splitext(file)[0] + ":" for file in files_in_directory]

    # Check if linker.txt exists
    if os.path.exists(linker_file):
        # Read existing entries in linker.txt
        with open(linker_file, 'r') as file:
            existing_entries = file.read().splitlines()
            for i, val in enumerate(existing_entries):
                existing_entries[i] = val.split(':')[0] + ":"
        # Add new entries
        new_entries = [file for file in files_without_extension if file not in existing_entries]
    else:
        # If linker.txt does not exist, all entries are new
        existing_entries = []
        new_entries = [file for file in files_without_extension]

    # Write (or append) to linker.txt
    with open(linker_file, 'a') as file:
        for entry in new_entries:
            file.write(entry + '\n')


# Votre fonction pour lister les fichiers linker et créer un embed
async def list_linker_file(ctx, directory=PERSO, linker_file=LINKER):
    if not os.path.exists(linker_file):
        print(f"Le fichier {linker_file} n'existe pas.")
        return

    embed = discord.Embed(title="Liste des personnages liés", color=0x00ff00)

    with open(linker_file, 'r') as linker:
        lines = linker.readlines()

    for line in lines:
        if ':' in line:
            parts = line.strip().split(':')
            filename = parts[0].strip()
            pseudo = parts[1].strip() if len(parts) > 1 and parts[1] != "" else "N/A"
            json_file_path = os.path.join(directory, filename + '.json')

            if os.path.exists(json_file_path):
                embed.add_field(name="SLUG", value=filename, inline=True)
                embed.add_field(name="JOUEUR", value=pseudo, inline=True)
                # Ajoute une ligne vide pour séparer les entrées
            else:
                print(f"Le fichier JSON {json_file_path} n'existe pas.")
        else:
            print(f"Format de ligne invalide: {line}")

    return embed


def disconnect_from_linker(pseudo, linker_file=LINKER):
    if not os.path.exists(linker_file):
        print(f"Le fichier {linker_file} n'existe pas.")
        return ""

    with open(linker_file, 'r') as linker:
        lines = linker.readlines()

    flag = False
    for i, val in enumerate(lines):
        if pseudo in val:
            flag = True
            lines[i] = lines[i].replace(pseudo, "")

    if flag:
        with open(linker_file, 'w') as file:
            file.writelines(lines)
        return 0
    else:
        return 1


def get_file_for_player(player, linker_file=LINKER, directory=PERSO):
    if not os.path.exists(linker_file):
        print(f"Le fichier {linker_file} n'existe pas.")
        return None

    with open(linker_file, 'r') as linker:
        lines = linker.readlines()

    for line in lines:
        # Parse the line to get the filename and pseudo
        if ':' in line:
            parts = line.strip().split(':')
            filename = parts[0].strip()
            pseudo = parts[1].strip() if len(parts) > 1 else "N/A"
            if pseudo == player:
                # Construct the full path to the JSON file
                json_file_path = os.path.join(directory, filename + '.json')
                return json_file_path
    return None


def get_connected_players(linker_file=LINKER):
    if not os.path.exists(linker_file):
        print(f"Le fichier {linker_file} n'existe pas.")
        return []

    connected_players = []

    with open(linker_file, 'r') as linker:
        lines = linker.readlines()

    for line in lines:
        # Parse the line to get the pseudo
        if ':' in line:
            parts = line.strip().split(':')
            if len(parts) > 1:
                pseudo = parts[1].strip()
                connected_players.append(pseudo)

    return connected_players

def get_slug_from_pseudo(pseudo, linker_file=LINKER):
    try:
        with open(linker_file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            slug, player_pseudo = map(str.strip, line.split(':'))
            if player_pseudo == pseudo:
                return slug
        return None
    except FileNotFoundError:
        print(f"Le fichier {linker_file} n'existe pas.")
        return None