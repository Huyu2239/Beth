from discord.ext import commands
import discord
import os
import json
import emoji as EM
if os.name == "nt":
    s = "\\"
elif os.name == "posix":
    s = "/"


class Registration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ver = "0.0.0"
        with open(f"json{s}server_data.json") as f:
            self.server_data = json.load(f)
        with open(f"json{s}contents.json") as f:
            self.contents = json.load(f)

    async def json_save(self):
        with open(f"json{s}server_data.json", "w") as f:
            json.dump(self.server_data, f, indent=4)

    @commands.command(aliases=["act", "on"])
    @commands.has_guild_permissions(view_audit_log=True)
    async def activate(self, ctx):
        data = self.server_data.get(str(ctx.guild.id))
        if data:
            await ctx.send("既に有効化されています。\n"
                           "先に`deactivate`コマンドで無効化してから使用してください。")
            return
        await ctx.send("このチャンネルをログチャンネルに指定します。\n"
                       "下のパネルよりログに残したい内容を選択してください。\n"
                       "（このパネルはピン止めすることをお勧めします）"
                       "無効化する場合は`deactivate`コマンドを使用してください。")

        em = discord.Embed(color=discord.Color.blue())
        em.add_field(name="\U0001f1e6: message_edit:off",
                     value="メッセージ編集時", inline=True)
        em.add_field(name="\U0001f1e7: message_delete:off",
                     value="メッセージ削除時", inline=True)
        em.add_field(name="\U0001f1e8: channel_name:off",
                     value="チャンネル更新時", inline=True)
        em.add_field(name="\U0001f1e9: channel_position:off",
                     value="チャンネル更新時", inline=True)

        panel = await ctx.send(embed=em)
        emojis = self.contents.get(self.ver).get("emojis")
        for reac in emojis:
            reac = EM.emojize(reac, use_aliases=True)
            await panel.add_reaction(reac)
        data = {
            "channel_id": ctx.channel.id,
            "panel_id": panel.id,
            "ver": self.ver,
            "events": {
                "message_edit": "off",
                "message_delete": "off",
                "channel_name": "off",
                "channel_position": "off"
            }
        }
        self.server_data[str(ctx.guild.id)] = data
        await self.json_save()

    @commands.command(aliases=["deact", "off"])
    @commands.has_guild_permissions(view_audit_log=True)
    async def deactivate(self, ctx):
        data = self.server_data.get(str(ctx.guild.id))
        if data is None:
            await ctx.send("このサーバーではまだ有効化されていません。\n"
                           "`activate`コマンドで有効化してください")
            return
        await ctx.send("解除します")
        panel_id = data.get("panel_id")
        channel = self.bot.get_channel(data.get("channel_id"))
        pnl = await channel.fetch_message(panel_id)
        await pnl.delete()
        self.server_data.pop(str(ctx.guild.id))
        await self.json_save()

    async def setting(self, payload, Bool=None):
        guild = self.bot.get_guild(payload.guild_id)
        data = self.server_data.get(str(guild.id))
        if data is None or payload.message_id != data.get("panel_id"):
            return
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = guild.get_member(payload.user_id)
        if member.bot:
            return
        emoji = EM.demojize(str(payload.emoji))
        ver = data.get("ver")
        events = data.get("events")
        per = member.guild_permissions
        contents = self.contents.get(ver)
        emojis = contents.get("emojis")
        event = contents.get("events")
        txt = ""
        if ver[0] == "0":
            if per.view_audit_log and emoji in emojis:
                count = 0
                for reac in message.reactions:
                    s = reac.count % 2
                    if s == 0:
                        txt = "on"
                    if s == 1:
                        txt = "off"
                    events[event[count]] = txt
                    count += 1
                    if count > len(emojis):
                        break
                await self.json_save()
                await self.update(message, data)
            else:
                if Bool:
                    await message.remove_reaction(str(payload.emoji), member)
                    return
        if ver[0] == "1":
            await message.remove_reaction(str(payload.emoji), member)

    async def update(self, message, data):
        embed = message.embeds[0]
        embed_dict = embed.to_dict()
        ver = data.get("ver")
        count = 0
        if ver[0] == "0":
            contents = self.contents.get(ver)
            while count < len(contents.get("emojis")):
                emoji = EM.emojize(contents.get("emojis")[count])
                event = contents.get("events")[count]
                s = data.get("events").get(event)
                name = f"{emoji}:{event}:{s}"
                embed_dict["fields"][count]["name"] = name
                count += 1
            name_edited_embed = discord.Embed.from_dict(embed_dict)
            await message.edit(embed=name_edited_embed)
        if ver[0] == "1":
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.setting(payload, 1)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        await self.setting(payload)


def setup(bot):
    bot.add_cog(Registration(bot))
