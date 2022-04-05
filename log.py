import logging
import sqlite3

import datetime

from discord.ext import commands
import discord
import discord.utils as utils


log = logging.getLogger(__name__)


class Log(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def log(self, ctx: commands.Context, ch: discord.TextChannel, dry: bool = False, limit: int = None):
        await ctx.send("Logging...")

        start = datetime.datetime.now()

        if dry:
            async for msg in ch.history(limit=100):
                log.info(f"message in {ch}: {msg.content}")
        else:
            db = sqlite3.connect(f"{ch.id}.db")
            cur = db.cursor()

            cur.execute("""CREATE TABLE messages (sf text, content text);""")

            async for msg in ch.history(limit=limit):
                content = utils.remove_markdown(msg.clean_content)
                cur.execute("INSERT INTO messages (sf, content) VALUES (?, ?);", (msg.id, content))
                db.commit()

        end = datetime.datetime.now()

        db.close()
        await ctx.reply(f"Finished logging {ch.id}. Took {(end - start).total_seconds()}s")


def setup(bot):
    bot.add_cog(Log(bot))
