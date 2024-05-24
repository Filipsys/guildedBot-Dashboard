import guilded
from guilded.ext import commands
from data.database.sqlite import *

class KickCog(commands.Cog):
  """The 'kick' cog."""

  def __init__(self, client):
    self.client = client
  
  @commands.command()
  @commands.has_server_permissions(kick_members = True)
  async def kick(self, ctx, m, *, reason = "No reason provided."):
    """Kick a member from the server."""

    check_guild_exists = cursor.execute("SELECT guild_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,)).fetchone()
    if check_guild_exists is None:
      return await ctx.send("Please run the `$start` command first.")

    member = await commands.MemberConverter().convert(ctx, str(m).replace("@", ""))

    await member.kick()

    await ctx.send(f"Kicked {member} for {reason}.")


def setup(client):
  client.add_cog(KickCog(client))