import random

import discord
from discord.ext import commands
from constantes import *

import tools as t

# Remplacez 'YOUR_BOT_TOKEN' par le token de votre bot
# Définir les intents
intents = discord.Intents.all()
intents.members = True
intents.message_content = True  # Pour accéder au contenu des messages

# Préfixe pour les commandes du bot
bot = commands.Bot(command_prefix='!', intents=intents)


def has_role(role_name):
    def predicate(ctx):
        role = discord.utils.get(ctx.author.roles, name=role_name)
        if role is None:
            raise commands.CheckFailure(f"User does not have the {role_name} role")
        ctx.command.role_name = role_name
        return True

    return commands.check(predicate)


@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user.name}')


@bot.command(name='ping')
@bot.check(has_role('MJ'))
async def ping(ctx):
    await ctx.send('Pong!')


@bot.command(name='lvlup')
@bot.check(has_role("MJ"))
async def lvlup(ctx, pseudo):
    if pseudo.toLowerCase() == "all":
        await ctx.send("Tout le monde à lvlup")
    else:
        await ctx.send(f"{pseudo} à lvlup")


@bot.command(name='d20')
async def d20(ctx):
    rand_num = random.randint(1, 20)
    await ctx.send(f'{rand_num}')


@bot.command(name='d6')
async def d6(ctx):
    rand_num = random.randint(1, 6)
    await ctx.send(f'{rand_num}')


@bot.command(name='d4')
async def d6(ctx):
    rand_num = random.randint(1, 4)
    await ctx.send(f'{rand_num}')


@bot.command(name='d', help='Renvoie un nombre aléatoire entre 1 et le nombre spécifié')
async def random_number(ctx, number: int):
    if number < 1:
        await ctx.send('Veuillez entrer un nombre supérieur à 0.')
    else:
        rand_num = random.randint(1, number)
        await ctx.send(f'{rand_num}')


@random_number.error
async def random_number_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Veuillez entrer un nombre.')


# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CheckFailure):
#         command_name = ctx.command.name if ctx.command else "unknown command"
#         user_name = ctx.author.name
#         role_name = getattr(ctx.command, 'role_name', 'the required')  # Récupère le nom du rôle stocké
#         print(f'ERROR: {command_name}: {user_name} n\'a pas le rôle {role_name}')
#     if isinstance(error, commands.CommandNotFound):
#         print(f'ERROR: Command not found : {ctx.message.content}')

@bot.command(name='connect', help='Connecte un joueur à un personnage en utilisant un slug.')
async def connect(ctx, slug: str):
    player_pseudo = ctx.author.name  # Obtenir le pseudo du joueur
    t.create_or_update_linker_file(PERSO, LINKER)
    result = t.update_linker_file(PERSO, LINKER, slug, player_pseudo)

    if result == "error_slug_not_found":
        await ctx.send(f"Erreur : Le slug '{slug}' ne correspond à aucun personnage existant.")
    elif result == "error_pseudo_already_taken":
        await ctx.send(f"Erreur : Le pseudo '{player_pseudo}' est déjà associé au slug '{slug}'.")
    else:
        await ctx.send('Connecté!')


@bot.command(name='plist', help='Déconnecte un joueur de son personnage en utilisant un slug.')
async def plist(ctx):
    t.create_or_update_linker_file(PERSO, LINKER)
    await ctx.send(t.list_linker_file(PERSO, LINKER))


@bot.command(name="disconnect")
async def disconnect(ctx):
    pseudo = ctx.author.name
    out = t.disconnect_from_linker(LINKER, pseudo)
    if out:
        await ctx.send("Vous n'étiez pas connecté(e)")
    else:
        await ctx.send("Déconnecté(e) avec succès !")


# Démarrez le bot
bot.run(TOKEN)
