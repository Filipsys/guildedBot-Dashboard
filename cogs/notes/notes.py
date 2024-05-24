import guilded

from guilded.ext import commands
from data.database.sqlite import *


class NotesCog(commands.Cog):
  """The 'notes' cog."""

  def __init__(self, client):
    self.client = client
  
  @commands.command(aliases = ["viewnotes", "view_notes", "note"])
  @commands.has_server_permissions(kick_members = True)
  async def notes(self, ctx, member):
    """View notes for a member."""

    if str(member)[0] == "@":
      member = await commands.MemberConverter().convert(ctx, str(member).replace("@", ""))
    else:
      member = await commands.MemberConverter().convert(ctx, member)

    check_guild_exists = cursor.execute("SELECT guild_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,)).fetchone()
    if check_guild_exists is None:
      return await ctx.send("Please run the `$start` command first.")
    
    get_notes = cursor.execute("SELECT note FROM user_notes WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id)).fetchall()

    if len(get_notes) == 0:
        return await ctx.send(f"{member} has no notes.")

    notes = ""
    for note in get_notes:
        notes += note[0] + "\n"  

    embed = guilded.Embed(title = f"{member}'s notes", description = notes)

    await ctx.send(embed = embed)


def setup(client):
  client.add_cog(NotesCog(client))