import guilded
from guilded.ext import commands
from data.database.sqlite import *


class SoftBanCog(commands.Cog):
  """The 'softban' cog."""

  def __init__(self, client):
    self.client = client
  
  def can_ban_members():
    check_inherit_guilded_permissions = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("INHERIT_GUILDED_PERMISSIONS", msg.guild.id)).fetchone()

    if check_inherit_guilded_permissions is not None:
      return commands.has_guild_permissions(ban_members = True)
    

    async def predicate(ctx):
      if ctx.guild is None:
        return False
      
      return ctx.author.guild_permissions.ban_members
    
    return commands.check(predicate)
  
  @commands.command()
  @commands.check(can_ban_members)
  async def softban(self, ctx, m, *, reason = "No reason provided."):
    """Softban a member from the server."""

    check_guild_exists = cursor.execute("SELECT guild_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,)).fetchone()
    if check_guild_exists is None:
      return await ctx.send("Please run the `$start` command first.")

    member = await commands.MemberConverter().convert(ctx, str(m).replace("@", ""))

    await member.ban()
    await member.unban()

    await ctx.send(f"Softbanned {member} for {reason}.")


def setup(client):
  client.add_cog(SoftBanCog(client))