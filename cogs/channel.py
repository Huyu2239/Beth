from discord.ext import commands
import discord


class channel_log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def lode_data(self):
        cog = self.bot.get_cog('Registration')
        self.server_data = cog.server_data

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        await self.lode_data()
        data = self.server_data.get(str(before.guild.id))
        if data is None:
            return
        channel = data.get("channel_id")
        events = data.get("events")
        ver = data.get("ver")
        if ver[0] == "0":
            # name
            check = events.get("channel_name")
            if before.name != after.name and check == "on":
                embed = discord.Embed(title="channel_name", color=discord.Color.blue())
                embed.add_field(name="channel", value=f"<#{before.id}>", inline=True)
                embed.add_field(name="before", value=f"```diff\n-{before.name}```", inline=True)
                embed.add_field(name="after", value=f"```diff\n+{after.name}```", inline=True)
                await self.bot.get_channel(channel).send(embed=embed)
            # posi
            check = events.get("channel_position")
            if before.position != after.position and check == "on":
                embed = discord.Embed(title="channel_position", color=discord.Color.blue())
                embed.add_field(name="channel", value=f"<#{before.id}>", inline=True)
                embed.add_field(name="before", value=f"```diff\n-{before.position}番目```", inline=True)
                embed.add_field(name="after", value=f"```diff\n+{after.position}番目```", inline=True)
                await self.bot.get_channel(channel).send(embed=embed)
        if ver[0] == "1":
            embed = discord.Embed(title="ERROR",
                                  discription='サポートサーバーまで問い合わせください',
                                  color=discord.Color.red())
            await self.bot.get_channel(channel).send(embed=embed)


def setup(bot):
    bot.add_cog(channel_log(bot))
