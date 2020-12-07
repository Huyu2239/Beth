from discord.ext import commands
import discord
import re


class message_log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def lode_data(self):
        cog = self.bot.get_cog('Registration')
        self.server_data = cog.server_data

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return
        await self.lode_data()
        data = self.server_data.get(str(before.guild.id))
        if data:
            events = data.get("events")
            check = events.get("message_edit")
            if check == 'on':
                ver = data.get('ver')
                embed = discord.Embed(title="message_edit", color=discord.Color.blue())
                if ver[0] == '0':
                    b_txt = re.sub('^', '-', before.clean_content, flags=re.MULTILINE)
                    a_txt = re.sub('^', '+', after.clean_content, flags=re.MULTILINE)
                    channel_id = data.get("channel_id")
                    embed.add_field(name="channel", value=f"<#{before.channel.id}>", inline=True)
                    embed.add_field(name="author", value=f"<@{before.author.id}>", inline=True)
                    url = f"https://ptb.discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id}"
                    embed.add_field(name="url", value=f"[リンク]({url})", inline=True)
                    content = f"```diff\n{b_txt}```\n```diff\n{a_txt}\n```"
                    embed.add_field(name="content", value=content, inline=True)
                if ver[0] == '1':
                    embed = discord.Embed(title="ERROR",
                                          description='[サポートサーバー](https://discord.gg/TNQVhAu9fk)まで問い合わせください',
                                          color=discord.Color.red())
                await self.bot.get_channel(channel_id).send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        await self.lode_data()
        data = self.server_data.get(str(message.guild.id))
        if data:
            events = data.get("events")
            check = events.get("message_delete")
            if check == 'on':
                ver = data.get('ver')
                embed = discord.Embed(title="message_delete", color=discord.Color.blue())
                if ver[0] == '0':
                    channel_id = data.get("channel_id")
                    embed.add_field(name="チャンネル", value=f"<#{message.channel.id}>", inline=True)
                    embed.add_field(name="author", value=f"<@{message.author.id}>", inline=True)
                    embed.add_field(name="content", value=f"```{message.clean_content}```", inline=False)
                if ver[0] == '1':
                    channel_id = data.get("channel_id")
                    embed = discord.Embed(title="ERROR",
                                          description='[サポートサーバー](https://discord.gg/TNQVhAu9fk)まで問い合わせください',
                                          color=discord.Color.red())
                await self.bot.get_channel(channel_id).send(embed=embed)


def setup(bot):
    bot.add_cog(message_log(bot))
