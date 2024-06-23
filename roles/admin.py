import services.roles as r
import json

import discord
from discord.ext import commands

from services import tools as t
from var.constantes import *


class Admin(commands.Cog):
    """Catégorie de commandes pour les MJ."""

    def __init__(self, bot):
        self.bot = bot


    @staticmethod
    def checkup():
        async def predicate(ctx):
            if not os.path.exists(LINKER):
                raise commands.CheckFailure(f"Le fichier {LINKER} n'existe pas.")
            return True

        return commands.check(predicate)

    @commands.command(name="set_mj", help="Selectionne un MJ")
    @commands.has_permissions(administrator=True)
    @checkup()
    async def set_mj(self, ctx, player: discord.Member = commands.parameter(description=": Mention de la personne qui va être le MJ")):
        async with semaphore:
            await r.add_role_to_member(ctx.guild, player.name, "MJ")

    @commands.command(name="init", help="Initialise les rôles et salons pour les personnages.")
    @commands.has_permissions(administrator=True)
    async def init(self, ctx):
        async with semaphore:
            guild = ctx.guild
            t.create_or_update_linker_file()

            # Lire le fichier linker et obtenir les slugs et pseudos
            linker_file = LINKER
            with open(linker_file, 'r') as f:
                lines = f.readlines()

            linker_data = [line.strip().split(':') for line in lines]
            slugs = [data[0].strip() for data in linker_data]

            # Créer le rôle MJ s'il n'existe pas déjà
            mj_role = discord.utils.get(guild.roles, name="MJ")
            if not mj_role:
                mj_role = await guild.create_role(name="MJ", color=discord.Color.yellow(), hoist=True)
                await ctx.send("\u2705 - Rôle 'MJ' créé.")

            # Créer les rôles pour chaque slug
            for slug in slugs:
                role = discord.utils.get(guild.roles, name=slug)
                if not role:
                    await guild.create_role(name=slug, hoist=True)
                    await ctx.send(f"\u2705 - Rôle '{slug}' créé.")

            # Créer la catégorie 'personnage'
            category = discord.utils.get(guild.categories, name="personnage")
            if not category:
                category = await guild.create_category("personnage")
                await ctx.send("\u2705 - Catégorie 'personnage' créée.")

            # Créer les salons pour chaque slug et mettre à jour le fichier JSON
            for slug in slugs:
                role = discord.utils.get(guild.roles, name=slug)
                channel = discord.utils.get(guild.channels, name=slug)
                if not channel:
                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
                        mj_role: discord.PermissionOverwrite(read_messages=True,send_messages=True)
                    }
                    new_channel = await guild.create_text_channel(slug, category=category, overwrites=overwrites)
                    await ctx.send(f"\u2705 - Salon '{slug}' créé pour le rôle '{slug}'.")

                    # Mettre à jour le fichier JSON avec l'ID du channel
                    json_file_path = f'{PERSO}{slug}.json'
                    if os.path.exists(json_file_path):
                        with open(json_file_path, 'r') as json_file:
                            data = json.load(json_file)
                        data['admin']['channel'] = new_channel.id
                        with open(json_file_path, 'w') as json_file:
                            json.dump(data, json_file, indent=4)
                    else:
                        await ctx.send(f"\u274C - Fichier JSON pour '{slug}' non trouvé.")

            # Créer le salon MJ
            mj_channel = discord.utils.get(guild.channels, name="mj")
            if not mj_channel:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    mj_role: discord.PermissionOverwrite(read_messages=True)
                }
                await guild.create_text_channel("mj", category=category, overwrites=overwrites)
                await ctx.send("\u2705 - Salon 'mj' créé pour le rôle 'MJ'.")

    @commands.command(name="ending", help="Nettoie les rôles et salons créés par la commande init.")
    @commands.has_permissions(administrator=True)
    @checkup()
    async def ending(self, ctx):
        async with semaphore:
            guild = ctx.guild

            # Lire le fichier linker et obtenir les slugs
            linker_file = LINKER
            try:
                with open(linker_file, 'r') as f:
                    lines = f.readlines()
            except FileNotFoundError:
                await ctx.send(f"\u274C - Le fichier {linker_file} n'existe pas.")
                return

            linker_data = [line.strip().split(':') for line in lines]
            slugs = [data[0].strip() for data in linker_data]

            mj_role = discord.utils.get(guild.roles, name="MJ")
            if mj_role:
                await mj_role.delete()

            # Supprimer les rôles pour chaque slug
            for slug in slugs:
                role = discord.utils.get(guild.roles, name=slug)
                if role:
                    await role.delete()
                    await ctx.send(f"\u2705 - Rôle '{slug}' supprimé.")

            # Supprimer la catégorie 'personnage' et tous les salons
            category = discord.utils.get(guild.categories, name="personnage")
            if category:
                for channel in category.channels:
                    await channel.delete()
                    await ctx.send(f"\u2705 - Salon '{channel.name}' supprimé.")
                await category.delete()
                await ctx.send("\u2705 - Catégorie 'personnage' supprimée.")

            # Mettre à jour les fichiers JSON
            for slug in slugs:
                json_file_path = f'{PERSO}{slug}.json'  # Remplacez par le chemin correct vers vos fichiers JSON
                if os.path.exists(json_file_path):
                    with open(json_file_path, 'r') as json_file:
                        data = json.load(json_file)
                    data['admin']['channel'] = ""  # Enlever l'ID du salon
                    data['admin']['last-msg'] = ""  # Enlever l'ID du dernier message
                    with open(json_file_path, 'w') as json_file:
                        json.dump(data, json_file, indent=4)
                    await ctx.send(f"\u2705 - Fichier JSON pour '{slug}' mis à jour.")

            os.remove(LINKER)
            await ctx.send(f"\u2705 - Tous les joueurs ont été déconnectés. Attention, les statistiques des incarnation n'ont pas été ré-initialisée")
async def setup(bot):
    await bot.add_cog(Admin(bot))