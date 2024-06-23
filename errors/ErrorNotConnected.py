class ErrorNotConnected(Exception):
    def __init__(self, player):
        self.player = player

    async def send_message(self, ctx):
        await ctx.send(f"\u274C - {self.player.name} n'est pas lié à une incarnation. Connectez vous avec !connect <slug>.")