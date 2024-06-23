import json
import os

import discord
from discord.ext import commands

from errors.ErrorNotConnected import ErrorNotConnected
from services import tools as t, update_stats as us, format_stats as fs
from var.constantes import *

class MJ(commands.Cog):
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

    @staticmethod
    def notCheckup():
        async def predicate(ctx):
            if os.path.exists(LINKER):
                raise commands.CheckFailure(f"Le fichier {LINKER} existe.")
            return True

        return commands.check(predicate)

    @staticmethod
    def has_role(role_name):
        async def predicate(ctx):
            role = discord.utils.get(ctx.author.roles, name=role_name)
            if role is None:
                raise commands.CheckFailure(f"User does not have the {role_name} role")
            ctx.command.role_name = role_name
            return True

        return commands.check(predicate)


    @commands.command(name='ping', help="Vérifier si le bot fonctionne")
    @has_role('MJ')
    async def ping(self, ctx):
        """
        Vérifier si le bot fonctionne.
        """
        await ctx.send('Pong!')

    @commands.command(name='lvlup', help="Ajoute un level à quelqu'un")
    @has_role("MJ")
    @checkup()
    async def lvlup(self, ctx, player: discord.Member = commands.parameter(description=": Mention du joueur lié à l'incarnation qui à level-up")):
        async with semaphore:
            file = t.get_file_for_player(player.name)
            if not file:
                error = ErrorNotConnected(player.name)
                await error.send_message(ctx)
                return
            us.lvl_up(file)
            await fs.update_character_stats_message(ctx.bot,file)
            await ctx.send(f"\u2705 - {player} à level up !")


    @commands.command(name='lvlup_all', help="Ajoute un level à toutes les incarnations")
    @has_role("MJ")
    @checkup()
    async def lvlup_all(self, ctx):
        """
        Ajoute un level à toutes les incarnations
        """
        pseudos = t.get_connected_players()
        for p in pseudos:
            member = discord.utils.get(ctx.guild.members, name=p)
            await self.lvlup(ctx, member)

    @commands.command(name="fdisconnect", help="Dé-lie de force un personnage et son incarnation")
    @has_role("MJ")
    @checkup()
    async def fdisconnect(self, ctx, player: discord.Member = commands.parameter(description=": Mention du joueur à dé-lier de son incarnation")):
        async with semaphore:
            out = t.disconnect_from_linker(player.name)
            if out:
                error = ErrorNotConnected(player.name)
                await error.send_message(ctx)
            else:
                await ctx.send(f"\u2705 - {player.name} délié(e) avec succès !")

    @commands.command(name="add_insanite", help="Ajoute de l'insanité à un personnage")
    @has_role("MJ")
    @checkup()
    async def add_insanite(self, ctx, player: discord.Member = commands.parameter(description=": Mention du joueur dont l'incarnation va gagner de l'insanité")):
        async with semaphore:
            file = t.get_file_for_player(player.name)
            if not file:
                error = ErrorNotConnected(player.name)
                await error.send_message(ctx)
                return
            us.add_insanite(file)
            await fs.update_character_stats_message(ctx.bot, file)
            await ctx.send(f"\u2705 - {player.name} à reçu 1 point d'insanité")

    @commands.command(name="remove_insanite", help="Retire de l'insanité à un personnage")
    @has_role("MJ")
    @checkup()
    async def remove_insanite(self, ctx, player: discord.Member= commands.parameter(description=": Mention du joueur dont l'incarnation va perdre de l'insanité")):
        async with semaphore:
            file = t.get_file_for_player(player.name)
            if not file:
                error = ErrorNotConnected(player.name)
                await error.send_message(ctx)
                return
            us.remove_insanite(file)
            await fs.update_character_stats_message(ctx.bot, file)
            await ctx.send(f"\u2705 - {player.name} à perdu 1 point d'insanité")

    @commands.command(name="remove_insanite_all", help="Retire de l'insanité à tous")
    @has_role("MJ")
    @checkup()
    async def remove_insanite_all(self, ctx):
        pseudos = t.get_connected_players()
        for p in pseudos:
            member = discord.utils.get(ctx.guild.members, name=p)
            await self.remove_insanite(ctx, member)

    @commands.command(name="add_insanite_all", help="Ajoute de l'insanité à tous")
    @has_role("MJ")
    @checkup()
    async def add_insanite_all(self, ctx):
        pseudos = t.get_connected_players()
        for p in pseudos:
            member = discord.utils.get(ctx.guild.members, name=p)
            await self.add_insanite(ctx, member)


    @commands.command(name="add_competence", help="Ajoute un niveau à une compétence de quelqu'un")
    @has_role("MJ")
    @checkup()
    async def add_competence(self,ctx,player: discord.Member = commands.parameter(description=": Mention du joueur dont l'incarnation va gagner un niveau de compétence") , competence_name:str = commands.parameter(description=": Nom de la compétence")):
        async with semaphore:
            file = t.get_file_for_player(player.name)
            if not file:
                error = ErrorNotConnected(player.name)
                await error.send_message(ctx)
                return
            us.add_competence(file,competence_name)
            await fs.update_character_stats_message(ctx.bot, file)
            await ctx.send(f"\u2705 - {player.name} à gagné un niveau en {competence_name}")
            return

    @commands.command(name="add_savoir", help="Ajoute un niveau à une compétence de quelqu'un")
    @has_role("MJ")
    @checkup()
    async def add_competence(self,ctx,player: discord.Member = commands.parameter(description=": Mention du joueur dont l'incarnation va gagner un niveau de compétence"), competence_name:str= commands.parameter(description=": Intitulé du savoir")):
        async with semaphore:
            file = t.get_file_for_player(player.name)
            if not file:
                error = ErrorNotConnected(player.name)
                await error.send_message(ctx)
                return
            us.add_competence(file,competence_name)
            await fs.update_character_stats_message(ctx.bot, file)
            await ctx.send(f"\u2705 - Le niveau du savoir '{competence_name}' a été augmenté de 1 pour {player.name}")
            return

    @commands.command(name="show_stats", help="Affiche les stats d'un joueur")
    @has_role("MJ")
    @checkup()
    async def show_stats(self,ctx,player: discord.Member):
        async with semaphore:
            file = t.get_file_for_player(player.name)
            if not file:
                error = ErrorNotConnected(player.name)
                await error.send_message(ctx)
                return
            embed = fs.aff_stat(file)
            await ctx.send(embed=embed)
            return

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
    await bot.add_cog(MJ(bot))
