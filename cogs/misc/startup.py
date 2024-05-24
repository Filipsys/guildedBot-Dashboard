import guilded
import time as time_module

from guilded.ext import commands
from data.database.sqlite import *


class StartupCog(commands.Cog):
  """The 'startup' cog."""

  def __init__(self, client):
    self.client = client
  
  @commands.command(aliases = ["startup", "begin", "init", "initialize", "setup"])
  @commands.has_server_permissions(administrator = True)
  async def start(self, ctx):
    """Start the bot."""

    check_guild_exists = cursor.execute("SELECT guild_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,)).fetchone()

    if check_guild_exists is not None:
      return await ctx.send("This server has already been set up. Type `$help` to see my list of available commands.")

    prefix = "$"

    try:
      cursor.execute("SELECT prefix FROM guilds WHERE guild_id = ?", (str(ctx.guild.id),))
      prefix = cursor.fetchone()[0]
      
      await ctx.send(f"This server has already been set up. Type `{prefix}help` to see my list of available commands.")
    except:
      cursor.execute("INSERT INTO guilds (guild_id, prefix) VALUES (?, ?)", (str(ctx.guild.id), "$"))
      cursor.execute("UPDATE bot_info_dashboard SET value = value + 1 WHERE variable = 'GUILD_COUNT'")
      database.commit()

      await ctx.send(f"Hello! Thanks for deciding to use this bot! To get started, run `{prefix}help` to see my commands or `{prefix}tutorial` to learn about my commands and features. (recommended for first-time users)")

    # cursor.execute("INSERT INTO command_history (user_name, user_id, guild_name, guild_id, command, time) VALUES (?, ?, ?, ?, ?, ?)", (ctx.author.name, ctx.author.id, ctx.guild.name, ctx.guild.id, ctx.command.name, int(time_module.time())))
    database.commit()


def setup(client):
  client.add_cog(StartupCog(client))