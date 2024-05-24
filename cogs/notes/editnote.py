import guilded

from guilded.ext import commands
from data.database.sqlite import *


class EditNoteCog(commands.Cog):
  """The 'editnote' cog."""

  def __init__(self, client):
    self.client = client
  
  @commands.command(aliases = ["edit_note"])
  @commands.has_server_permissions(kick_members = True)
  async def editnote(self, ctx, member, old_note, new_note):
    """Ban a member from the server."""

    if str(member)[0] == "@":
      member = await commands.MemberConverter().convert(ctx, str(member).replace("@", ""))
    else:
      member = await commands.MemberConverter().convert(ctx, member)

    if old_note == new_note:
      return await ctx.send("The old note and the new note cannot be the same.")

    check_guild_exists = cursor.execute("SELECT guild_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,)).fetchone()
    if check_guild_exists is None:
      return await ctx.send("Please run the `$start` command first.")
    
    get_note = cursor.execute("SELECT note FROM user_notes WHERE guild_id = ? AND user_id = ? AND note = ?", (ctx.guild.id, member.id, old_note)).fetchone()

    if get_note is None:
      return await ctx.send(f"{member} has no note with the content '{old_note}'.")
    
    cursor.execute("UPDATE user_notes SET note = ? WHERE guild_id = ? AND user_id = ? AND note = ?", (new_note, ctx.guild.id, member.id, old_note))

    await ctx.send(f"Edited note `{old_note}` to `{new_note}` for {member}.")


def setup(client):
  client.add_cog(EditNoteCog(client))