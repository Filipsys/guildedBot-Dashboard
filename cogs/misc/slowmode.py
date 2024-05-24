import guilded
from guilded.ext import commands
from sqlite import *


class SlowmodeCog(commands.Cog):
  """The 'slowmode' count cog."""

  def __init__(self, client):
    self.client = client

  @commands.command(aliases = ["sm"])
  @commands.has_server_permissions(manage_channels = True)
  async def slowmode(self, ctx, seconds: int = 5):

    check_guild_exists = cursor.execute("SELECT guild_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,)).fetchone()
    if check_guild_exists is None:
      return await ctx.send("Please run the `$start` command first.")
    
    if seconds > 21600:
      return await ctx.send("You can only set slowmode up to 6 hours.")
    
    await ctx.channel.edit(rate_limit_per_user = seconds)

    await ctx.send(f"Set the slowmode delay to {seconds} seconds.")


def setup(client):
  client.add_cog(SlowmodeCog(client))