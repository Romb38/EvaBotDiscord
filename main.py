import discord
from discord.ext import commands

from var.constantes import *

# Définir les intents
intents = discord.Intents.all()
intents.members = True
intents.message_content = True  # Pour accéder au contenu des messages

# Préfixe pour les commandes du bot
bot = commands.Bot(command_prefix='!', intents=intents)


async def load_extensions():
    initial_extensions = ['roles.mj', 'roles.incarnation']
    for extension in initial_extensions:
        await bot.load_extension(extension)


@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user.name}')


async def main():
    await load_extensions()
    await bot.start(TOKEN)


if __name__ == '__main__':
    asyncio.run(main())
