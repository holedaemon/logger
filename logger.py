import logging

from discord.ext import commands
import discord


log = logging.getLogger(__name__)


class Logger(commands.Bot):
    """A Discord bot that logs channels to plaintext, for AI training."""

    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned)

        try:
            self.load_extension("log")
        except commands.ExtensionError as e:
            log.error(f"error importing extenstion: {e}")

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        await self.process_commands(message)

    async def on_command_error(self, ctx: commands.Context, exception):
        await ctx.reply(f"An error occurred during execution: {exception}")
