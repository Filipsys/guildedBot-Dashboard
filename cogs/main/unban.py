import guilded

from guilded.ext import commands
from data.database.sqlite import *


class UnbanCog(commands.Cog):
  """The 'unban' cog."""

  def __init__(self, client):
    self.client = client
  
  @commands.command()
  @commands.has_server_permissions(ban_members = True)
  async def unban(self, ctx, m):
    """Unban a member from the server."""

    check_guild_exists = cursor.execute("SELECT guild_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,)).fetchone()
    if check_guild_exists is None:
      return await ctx.send("Please run the `$start` command first.")

    member = await commands.MemberConverter().convert(ctx, str(m).replace("@", ""))

    await member.unban()

    await ctx.send(f"Unbanned {member}.")


def setup(client):
  client.add_cog(UnbanCog(client))