import guilded

from guilded.ext import commands
from data.database.sqlite import *


class AddNoteCog(commands.Cog):
  """The 'addnote' cog."""

  def __init__(self, client):
    self.client = client
  
  @commands.command(aliases = ["add_note"])
  @commands.has_server_permissions(kick_members = True)
  async def addnote(self, ctx, member, *, note):
    """Ban a member from the server."""

    if note is None:
      return await ctx.send("Please provide a note.")

    if str(member)[0] == "@":
      member = await commands.MemberConverter().convert(ctx, str(member).replace("@", ""))
    else:
      member = await commands.MemberConverter().convert(ctx, member)

    check_guild_exists = cursor.execute("SELECT guild_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,)).fetchone()
    if check_guild_exists is None:
      return await ctx.send("Please run the `$start` command first.")
    
    cursor.execute("INSERT INTO user_notes (guild_id, user_id, note) VALUES (?, ?, ?)", (ctx.guild.id, member.id, note))    
    database.commit()

    await ctx.send(f"Added note to {member}.")


def setup(client):
  client.add_cog(AddNoteCog(client))