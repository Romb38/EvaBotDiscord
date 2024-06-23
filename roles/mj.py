import json

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
            out,code = us.add_competence(file,competence_name)
            if not code:
                await fs.update_character_stats_message(ctx.bot, file)
            await ctx.send(out)
            return

    @commands.command(name="add_savoir", help="Ajoute un niveau à une compétence de quelqu'un")
    @has_role("MJ")
    @checkup()
    async def add_savoir(self,ctx,player: discord.Member = commands.parameter(description=": Mention du joueur dont l'incarnation va gagner un niveau de compétence"), competence_name:str= commands.parameter(description=": Intitulé du savoir")):
        async with semaphore:
            file = t.get_file_for_player(player.name)
            if not file:
                error = ErrorNotConnected(player.name)
                await error.send_message(ctx)
                return
            out, code = us.add_savoir(file,competence_name)
            if not code:
                await fs.update_character_stats_message(ctx.bot, file)
            await ctx.send(out)
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

    @commands.command(name="set_stats", help="Met à jour les statistiques d'un joueur")
    @has_role("MJ")
    @checkup()
    async def set_stats(self,ctx,player: discord.Member= commands.parameter(description=": Mention du joueur concerné"), value:int = commands.parameter(description=": Valeur à placer dans la stat"), stat:str = commands.parameter(description=": Stat à modifier")):
        async with semaphore:
            file = t.get_file_for_player(player.name)
            if not file:
                error = ErrorNotConnected(player.name)
                await error.send_message(ctx)
                return
            out,code = us.set_stat(file,stat,value)
            if not code:
                await fs.update_character_stats_message(ctx.bot, file)
            await ctx.send(out)
            return
async def setup(bot):
    await bot.add_cog(MJ(bot))
