import guilded

from guilded.ext import commands
from data.database.sqlite import *


class AddRoleCog(commands.Cog):
  """The 'addrole' cog."""

  def __init__(self, client):
    self.client = client
  
  @commands.command(aliases = ["addrole"])
  @commands.has_server_permissions(manage_roles = True)
  async def add_role(self, ctx, member, role):
    """Add a role to a member."""

    check_guild_exists = cursor.execute("SELECT guild_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,)).fetchone()
    if check_guild_exists is None:
      return await ctx.send("Please run the `$start` command first.")
    

    if str(role)[0] == "@":
      role = await commands.RoleConverter().convert(ctx, str(role).replace("@", ""))
    else:
      role = await commands.RoleConverter().convert(ctx, role)

    if str(member)[0] == "@":
      member = await commands.MemberConverter().convert(ctx, str(member).replace("@", ""))
    else:
      member = await commands.MemberConverter().convert(ctx, member)

    await member.add_roles(role)

    await ctx.send(f"Added the role {role} to {member}.")


def setup(client):
  client.add_cog(AddRoleCog(client))