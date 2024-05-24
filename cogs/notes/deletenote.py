import guilded

from guilded.ext import commands
from data.database.sqlite import *


class DeleteNoteCog(commands.Cog):
  """The 'deletenote' cog."""

  def __init__(self, client):
    self.client = client
  
  @commands.command(aliases = ["deletenote"])
  @commands.has_server_permissions(kick_members = True)
  async def deletenote(self, ctx, member, note):
    """Ban a member from the server."""

    if str(member)[0] == "@":
      member = await commands.MemberConverter().convert(ctx, str(member).replace("@", ""))
    else:
      member = await commands.MemberConverter().convert(ctx, member)

    check_guild_exists = cursor.execute("SELECT guild_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,)).fetchone()
    if check_guild_exists is None:
      return await ctx.send("Please run the `$start` command first.")
    
    get_note = cursor.execute("SELECT note FROM user_notes WHERE guild_id = ? AND user_id = ? AND note = ?", (ctx.guild.id, member.id, note)).fetchone()

    if get_note is None:
      return await ctx.send(f"{member} has no note with the content '{note}'.")
    
    cursor.execute("DELETE FROM user_notes WHERE guild_id = ? AND user_id = ? AND note = ?", (ctx.guild.id, member.id, note))
    database.commit()

    await ctx.send(f"Deleted note `{note}` from {member}.")


def setup(client):
  client.add_cog(DeleteNoteCog(client))