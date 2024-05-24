import guilded

from guilded.ext import commands
from BOTS.default.data.database.sqlite import *


class PrefixCog(commands.Cog):
  """The 'prefix' cog."""

  def __init__(self, client):
    self.client = client
  
  @commands.command()
  @commands.has_server_permissions(kick_members = True)
  async def prefix(self, ctx, prefix):
    """Change the bot's prefix."""

    cursor.execute("UPDATE guilds SET prefix = ? WHERE guild_id = ?", (prefix, str(ctx.guild.id)))
    database.commit()


def setup(client):
  client.add_cog(PrefixCog(client))