import guilded
import time as time_module
from guilded.ext import commands
from data.database.sqlite import *

class BanCog(commands.Cog):
  """The 'ban' cog."""

  def __init__(self, client):
    self.client = client
  
  @commands.command(aliases = ["banish", "begone"])
  @commands.has_server_permissions(ban_members = True)
  async def ban(self, ctx, m, *, reason = "No reason provided."):
    """Ban a member from the server."""

    check_guild_exists = cursor.execute("SELECT guild_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,)).fetchone()
    if check_guild_exists is None:
      return await ctx.send("Please run the `$start` command first.")
    
    if str(m)[0] == "<":
      member = await commands.MemberConverter().convert(ctx, str(m).replace("@", "").replace("!", "").replace("<", "").replace(">", "").replace("&", ""))
    else:
      member = await commands.MemberConverter().convert(ctx, m)

    await member.ban()

    cursor.execute("INSERT INTO mod_command_history (target_id, target_name, executor_id, executor_name, executor_profile_picture_url, executor_role, guild_id, guild_name, action, timestamp, reason) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (str(member.id), str(member.name), str(ctx.author.id), str(ctx.author.name), str(ctx.author.avatar), "Moderator", str(ctx.guild.id), str(ctx.guild.name), "ban", int(time_module.time()), reason))
    database.commit()

    await ctx.send(f"Banned {member} for {reason}.")


def setup(client):
  client.add_cog(BanCog(client))