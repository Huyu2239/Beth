from discord.ext import commands
import discord


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="main", color=discord.Color.blue())
        embed.add_field(name="@Beth help", value="コマンド一覧表示", inline=False)
        embed.add_field(name="@Beth activate [act, on]",
                        value="ログ有効化", inline=False)
        embed.add_field(name="@Beth deactivate [deact, off]",
                        value="ログ無効化", inline=False)
        embed.add_field(name="サポートサーバー",
                        value="[リンク](https://discord.gg/TNQVhAu9fk)",
                        inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
