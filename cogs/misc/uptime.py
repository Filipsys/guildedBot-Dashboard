import guilded
import datetime

from guilded.ext import commands
from data.misc.uptime import get_uptime


class UptimeCog(commands.Cog):
  """The uptime cog."""

  def __init__(self, client):
    self.client = client

  @commands.command(aliases = ["uptime"])
  async def uptime_command(self, ctx):
    """Shows the uptime of the bot."""

    uptime_now = datetime.datetime.now() - get_uptime()
    await ctx.send(f"I have been online for {str(uptime_now)[:-7]}.")

def setup(client):
  client.add_cog(UptimeCog(client))