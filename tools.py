import os


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