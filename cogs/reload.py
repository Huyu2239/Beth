from discord.ext import commands
import os


class Relode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reload(self, ctx):
        if not await self.bot.is_owner(ctx.author):
            return
        msg = await ctx.send('再読み込み中・・・')
        for cog in os.listdir("./cogs"):
            if cog.endswith(".py") and cog != 'reload.py':
                try:
                    self.bot.load_extension(f"cogs.{cog[:-3]}")
                except commands.ExtensionAlreadyLoaded:
                    self.bot.reload_extension(f"cogs.{cog[:-3]}")
        await msg.edit(content='読み込みました')


def setup(bot):
    bot.add_cog(Relode(bot))
