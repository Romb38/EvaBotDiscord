import random

from discord.ext import commands

import roles as r
import format_stats as fs
import tools as t
import update_stats as us


class Incarnation(commands.Cog):
    """Catégorie de commandes pour les incarnations."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='d20', help="Lance un dé à 20 faces")
    async def d20(self, ctx):
        rand_num = random.randint(1, 20)
        await ctx.send(f'{rand_num}')

    @commands.command(name='d6', help="Lance un dé à 6 faces")
    async def d6(self, ctx):
        rand_num = random.randint(1, 6)
        await ctx.send(f'{rand_num}')

    @commands.command(name='d4', help="Lance un dé à 4 faces")
    async def d4(self, ctx):
        rand_num = random.randint(1, 4)
        await ctx.send(f'{rand_num}')

    @commands.command(name='d', help='Renvoie un nombre aléatoire entre 1 et le nombre spécifié')
    async def random_number(self, ctx, number: int = commands.parameter(description=": Valeur maximale du dé (incluse)")):
        if number < 1:
            await ctx.send('Veuillez entrer un nombre supérieur à 0.')
        else:
            rand_num = random.randint(1, number)
            await ctx.send(f'{rand_num}')

    @commands.command(name='connect', help='Lie un joueur à une incarnation en utilisant un slug.')
    async def connect(self, ctx, slug: str = commands.parameter(description=": Slug de l'incarnation (généralement nom_prenom)")):
        player_pseudo = ctx.author.name  # Obtenir le pseudo du joueur
        t.create_or_update_linker_file()
        result = t.update_linker_file(slug, player_pseudo)


        if result == "error_slug_not_found":
            await ctx.send(f"Erreur : Le slug '{slug}' ne correspond à aucun personnage existant.")
        elif result == "error_pseudo_already_taken":
            await ctx.send(f"Erreur : Le pseudo '{player_pseudo}' est déjà associé au slug '{slug}'.")
        else:
            await r.add_role_to_member(ctx.guild,player_pseudo,slug)
            file = t.get_file_for_player(ctx.author.name)
            await fs.update_character_stats_message(ctx.bot, file)
            await ctx.send('Connecté!')

    @commands.command(name='plist', help='Liste les incarnations et leurs joueurs')
    async def plist(self, ctx):
        t.create_or_update_linker_file()
        await ctx.send(t.list_linker_file())

    @commands.command(name="disconnect", help="Dé-lie un joueur et son incarnation")
    async def disconnect(self, ctx):
        t.create_or_update_linker_file()
        pseudo = ctx.author.name
        slug = t.get_slug_from_pseudo(pseudo)
        out = t.disconnect_from_linker(pseudo)
        if out:
            await ctx.send("Vous n'étiez pas connecté(e)")
        else:
            await r.remove_role_from_member(ctx.guild,pseudo,slug)
            await ctx.send("Déconnecté(e) avec succès !")

    @commands.command(name="add", help="Ajoute une valeur aux statistiques")
    async def add(self, ctx, count:int= commands.parameter(description=": Valeur de l'augmentation"), stats:str= commands.parameter(description=": Nom de la stat à améliorer")):
        file = t.get_file_for_player(ctx.author.name)
        if not file:
            await ctx.send("Vous n'êtes pas connecté à une incarnation, connectez-vous avec !connect <slug>")
            return
        elif count <= 0:
            await ctx.send("Vous ne pouvez pas ajouter ce nombre à vos stats. Rien n'a été fait")
            return
        else:
            out = us.add_stats(file, stats, count)
            await fs.update_character_stats_message(ctx.bot, file)
            await ctx.send(out)

async def setup(bot):
    await bot.add_cog(Incarnation(bot))
