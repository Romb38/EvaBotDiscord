import json

import discord
from discord.ext import commands

import format_stats as fs
import tools as t
import update_stats as us
from constantes import *


class MJ(commands.Cog):
    """Catégorie de commandes pour les MJ."""

    def __init__(self, bot):
        self.bot = bot

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
        await ctx.send('Pong!')

    @commands.command(name='lvlup', help="Ajoute un level à quelqu'un")
    @has_role("MJ")
    async def lvlup(self, ctx, player: discord.Member):
        file = t.get_file_for_player(player.name)
        if not file:
            await ctx.send(f"{player.name} n'est pas lié à une incarnation")
            return
        us.lvl_up(file)
        await fs.update_character_stats_message(ctx.bot,file)
        await ctx.send(f"{player} à level up !")


    @commands.command(name='lvlup_all')
    @has_role("MJ")
    async def lvlup_all(self, ctx):
        pseudos = t.get_connected_players()
        for p in pseudos:
            member = discord.utils.get(ctx.guild.members, name=p)
            await self.lvlup(ctx, member)

    @commands.command(name="fdisconnect", help="Dé-lie de force un personnage et son incarnation")
    @has_role("MJ")
    async def fdisconnect(self, ctx, player: discord.Member):
        out = t.disconnect_from_linker(player.name)
        if out:
            await ctx.send(f"{player.name} n'était pas lié(e) à une incarnation")
        else:
            await ctx.send(f"{player.name} délié(e) avec succès !")

    @commands.command(name="add_insanite", help="Ajoute de l'insanité à un personnage")
    @has_role("MJ")
    async def add_insanite(self, ctx, player: discord.Member):
        file = t.get_file_for_player(player.name)
        if not file:
            await ctx.send(f"{player.name} n'est pas lié à une incarnation")
            return
        us.add_insanite(file)
        await fs.update_character_stats_message(ctx.bot, file)
        await ctx.send(f"{player.name} à reçu 1 point d'insanité")

    @commands.command(name="remove_insanite", help="Ajoute de l'insanité à un personnage")
    @has_role("MJ")
    async def remove_insanite(self, ctx, player: discord.Member):
        file = t.get_file_for_player(player.name)
        if not file:
            await ctx.send(f"{player.name} n'est pas lié à une incarnation")
            return
        us.remove_insanite(file)
        await fs.update_character_stats_message(ctx.bot, file)
        await ctx.send(f"{player.name} à perdu 1 point d'insanité")

    @commands.command(name="remove_insanite_all", help="Retire de l'insanité à tous")
    @has_role("MJ")
    async def remove_insanite_all(self, ctx):
        pseudos = t.get_connected_players()
        for p in pseudos:
            member = discord.utils.get(ctx.guild.members, name=p)
            await self.remove_insanite(ctx, member)

    @commands.command(name="add_insanite_all", help="Ajoute de l'insanité à tous")
    @has_role("MJ")
    async def add_insanite_all(self, ctx):
        pseudos = t.get_connected_players()
        for p in pseudos:
            member = discord.utils.get(ctx.guild.members, name=p)
            await self.add_insanite(ctx, member)


    @commands.command(name="add_competence", help="Ajoute un niveau à une compétence de quelqu'un")
    @has_role("MJ")
    async def add_competence(self,ctx,player: discord.Member, competence_name:str):
        file = t.get_file_for_player(player.name)
        if not file:
            await ctx.send(f"{player.name} n'est pas lié à une incarnation")
            return
        us.add_competence(file,competence_name)
        await fs.update_character_stats_message(ctx.bot, file)
        return

    @commands.command(name="add_savoir", help="Ajoute un niveau à une compétence de quelqu'un")
    @has_role("MJ")
    async def add_competence(self,ctx,player: discord.Member, competence_name:str):
        file = t.get_file_for_player(player.name)
        if not file:
            await ctx.send(f"{player.name} n'est pas lié à une incarnation")
            return
        us.add_competence(file,competence_name)
        await fs.update_character_stats_message(ctx.bot, file)
        return

    @commands.command(name="show_stats", help="Affiche les stats d'un joueur")
    @has_role("MJ")
    async def show_stats(self,ctx,player: discord.Member):
        file = t.get_file_for_player(player.name)
        if not file:
            await ctx.send(f"{player.name} n'est pas lié à une incarnation")
            return
        embed = fs.aff_stat(file)
        await ctx.send(embed=embed)
        return

    @commands.command(name="init", help="Initialise les rôles et salons pour les personnages.")
    @commands.has_permissions(administrator=True)
    async def init(self, ctx):
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
            await ctx.send("Rôle 'MJ' créé.")

        # Créer les rôles pour chaque slug
        for slug in slugs:
            role = discord.utils.get(guild.roles, name=slug)
            if not role:
                role = await guild.create_role(name=slug, hoist=True)
                await ctx.send(f"Rôle '{slug}' créé.")

        # Créer la catégorie 'personnage'
        category = discord.utils.get(guild.categories, name="personnage")
        if not category:
            category = await guild.create_category("personnage")
            await ctx.send("Catégorie 'personnage' créée.")

        # Créer les salons pour chaque slug et mettre à jour le fichier JSON
        for slug in slugs:
            role = discord.utils.get(guild.roles, name=slug)
            channel = discord.utils.get(guild.channels, name=slug)
            if not channel:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    role: discord.PermissionOverwrite(read_messages=True),
                    mj_role: discord.PermissionOverwrite(read_messages=True)
                }
                new_channel = await guild.create_text_channel(slug, category=category, overwrites=overwrites)
                await ctx.send(f"Salon '{slug}' créé pour le rôle '{slug}'.")

                # Mettre à jour le fichier JSON avec l'ID du channel
                json_file_path = f'{PERSO}{slug}.json'
                if os.path.exists(json_file_path):
                    with open(json_file_path, 'r') as json_file:
                        data = json.load(json_file)
                    data['admin']['channel'] = new_channel.id
                    with open(json_file_path, 'w') as json_file:
                        json.dump(data, json_file, indent=4)
                else:
                    await ctx.send(f"Fichier JSON pour '{slug}' non trouvé.")

        # Créer le salon MJ
        mj_channel = discord.utils.get(guild.channels, name="mj")
        if not mj_channel:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                mj_role: discord.PermissionOverwrite(read_messages=True)
            }
            await guild.create_text_channel("mj", category=category, overwrites=overwrites)
            await ctx.send("Salon 'mj' créé pour le rôle 'MJ'.")

    @commands.command(name="ending", help="Nettoie les rôles et salons créés par la commande init.")
    @commands.has_permissions(administrator=True)
    async def ending(self, ctx):
        guild = ctx.guild

        # Lire le fichier linker et obtenir les slugs
        linker_file = LINKER
        try:
            with open(linker_file, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            await ctx.send(f"Le fichier {linker_file} n'existe pas.")
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
                await ctx.send(f"Rôle '{slug}' supprimé.")

        # Supprimer la catégorie 'personnage' et tous les salons
        category = discord.utils.get(guild.categories, name="personnage")
        if category:
            for channel in category.channels:
                await channel.delete()
                await ctx.send(f"Salon '{channel.name}' supprimé.")
            await category.delete()
            await ctx.send("Catégorie 'personnage' supprimée.")

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
                await ctx.send(f"Fichier JSON pour '{slug}' mis à jour.")

        # Vider le fichier linker.txt
        with open(linker_file, 'w') as f:
            f.write("")
        await ctx.send(f"Tous les joueurs ont été déconnectés.")
async def setup(bot):
    await bot.add_cog(MJ(bot))
