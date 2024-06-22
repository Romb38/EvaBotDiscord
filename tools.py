import os
import json


def update_linker_file(directory, linker_file, slug, player_pseudo):
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


def create_or_update_linker_file(directory, linker_file):
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
        new_entries = [file + ':' for file in files_without_extension]

    # Write (or append) to linker.txt
    with open(linker_file, 'a') as file:
        for entry in new_entries:
            file.write(entry + '\n')


def list_linker_file(directory='.', linker_file='linker.txt'):
    if not os.path.exists(linker_file):
        print(f"Le fichier {linker_file} n'existe pas.")
        return ""

    results = ["SLUG\tNOM\tPRENOM\tJOUEUR"]

    with open(linker_file, 'r') as linker:
        lines = linker.readlines()

    for line in lines:
        # Parse the line to get the filename and pseudo
        if ':' in line:
            parts = line.strip().split(':')
            filename = parts[0].strip()
            pseudo = parts[1].strip() if len(parts) > 1 and parts[1] != "" else "N/A"

            # Construct the full path to the JSON file
            json_file_path = os.path.join(directory, filename + '.json')

            if os.path.exists(json_file_path):
                # Read the JSON file
                with open(json_file_path, 'r') as json_file:
                    data = json.load(json_file)
                    nom = data.get('nom', 'N/A')
                    prenom = data.get('prenom', 'N/A')
                    results.append(f"{filename}\t{nom}\t{prenom}\t{pseudo}")
            else:
                print(f"Le fichier JSON {json_file_path} n'existe pas.")
        else:
            print(f"Format de ligne invalide: {line}")

    # Combine results into a single string
    result_string = "\n".join(results)
    return result_string


def disconnect_from_linker(linker_file, pseudo):
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
