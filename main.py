import os
import discord
from discord.ext import commands
import traceback
from dotenv import load_dotenv
load_dotenv()


class Beth(commands.Bot):
    def __init__(self, command_prefix, **options):
        prefix = command_prefix  # commands.when_mentioned_or(command_prefix)
        allowed_mentions = discord.AllowedMentions(everyone=False,
                                                   roles=False,
                                                   users=True)
        intents = discord.Intents.all()
        super().__init__(command_prefix=prefix,
                         intents=intents,
                         allowed_mentions=allowed_mentions,
                         **options)
        self.prefix = command_prefix
        self.logch_id = 779990306434842646  # error-log
        self.remove_command('help')

    async def on_ready(self):
        cogs = [
            'reload',
            'help',
            'registration',
            'message',
            'channel'
        ]
        for cog in cogs:
            try:
                self.load_extension(f"cogs.{cog}")
            except commands.ExtensionAlreadyLoaded:
                self.reload_extension(f"cogs.{cog}")
        print('-----')
        print('起動')
        print('-----')
        await self.change_presence(activity=discord.Game(name="@Beth help"))

    async def on_command_error(self, ctx, error1):
        if error1 == commands.CommandNotFound:
            pass
        orig_error = getattr(error1, "original", error1)
        error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
        error_msg = "```py\n" + error_msg + "\n```"
        try:
            await self.get_channel(self.logch_id).send(error_msg)
        except discord.errors.HTTPException:
            print(error_msg)


if __name__ == '__main__':
    bot = Beth(command_prefix="t.", max_messages=9999)
    bot.run(os.environ['TOKEN'])
