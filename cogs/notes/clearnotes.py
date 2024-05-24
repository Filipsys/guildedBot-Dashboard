import guilded

from guilded.ext import commands
from data.database.sqlite import *


class ClearNotesCog(commands.Cog):
  """The 'clearnotes' cog."""

  def __init__(self, client):
    self.client = client
  
  @commands.command(aliases = ["clear_notes", "clearnote", "deletenotes", "delete_notes"])
  @commands.has_server_permissions(kick_members = True)
  async def clearnotes(self, ctx, member):
    """Ban a member from the server."""

    if str(member)[0] == "@":
      member = await commands.MemberConverter().convert(ctx, str(member).replace("@", ""))
    else:
      member = await commands.MemberConverter().convert(ctx, member)

    check_guild_exists = cursor.execute("SELECT guild_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,)).fetchone()
    if check_guild_exists is None:
      return await ctx.send("Please run the `$start` command first.")
    
    notes = cursor.execute("SELECT note FROM user_notes WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id)).fetchall()

    if len(notes) == 0:
      return await ctx.send(f"{member} has no notes.")
    
    cursor.execute("DELETE FROM user_notes WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id))
    database.commit()

    await ctx.send(f"Cleared notes for {member}.")


def setup(client):
  client.add_cog(ClearNotesCog(client))