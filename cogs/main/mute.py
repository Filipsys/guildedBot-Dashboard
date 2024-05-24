import guilded
import time as time_module

from guilded.ext import commands
from data.misc.variables import *
from data.database.sqlite import *


class MuteCog(commands.Cog):
  """The 'mute' cog."""

  def __init__(self, client):
    self.client = client

  @commands.command()
  async def mute(self, ctx, m, time: str, reason: str = None):
    """The 'mute' command."""

    check_guild_exists = cursor.execute("SELECT guild_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,)).fetchone()
    if check_guild_exists is None:
      return await ctx.send("Please run the `$start` command first.")

    member = await commands.MemberConverter().convert(ctx, str(m).replace("@", "").replace("<", "").replace(">", "").replace("!", "").replace("&", ""))

    original_time = time
    if any(unit in time for unit in ["minutes", "minute", "mins", "min", "m"]):
      time = time.replace("minutes", "").replace("minute", "").replace("mins", "").replace("min", "").replace("m", "")
    elif any(unit in time for unit in ["hours", "hour", "hrs", "hr", "h"]):
      time = time.replace("hours", "").replace("hour", "").replace("hrs", "").replace("hr", "").replace("h", "")
    elif any(unit in time for unit in ["days", "day", "d"]):
      time = time.replace("days", "").replace("day", "").replace("d", "")
    elif any(unit in time for unit in ["weeks", "week", "w"]):
      time = time.replace("weeks", "").replace("week", "").replace("w", "")
    elif any(unit in time for unit in ["months", "month", "mo", "m"]):
      time = time.replace("months", "").replace("month", "").replace("mo", "").replace("m", "")


    muted_role = cursor.execute("SELECT value FROM guild_variables WHERE guild_id = ? AND variable = ?", (ctx.guild.id, "MUTED_ROLE")).fetchone()
    
    if not muted_role:
      embed = guilded.Embed(
        title = "⚠️ Error",
        description = "The muted role was not set up yet. To fix this, please set the muted role ID using the `$settings change muted_role <role_id>` command.",
        color = guilded.Color.red()
      )

      return await ctx.reply(embed = embed)
    

    roles = await guilded.Server.fetch_roles(ctx.guild)
    found_muted_role = None

    for role in roles:
      if role.id == int(muted_role[0]):
        found_muted_role = role
        break

    if not found_muted_role:
      embed = guilded.Embed(
        title = "⚠️ Error",
        description = "The muted role was not found on the server. Please make sure the muted role ID is correct.",
        color = guilded.Color.red()
      )

      return await ctx.reply(embed = embed)
    
    await member.add_role(found_muted_role)

    amount_seconds_mute = 0
    if any(unit in original_time for unit in ["minutes", "minute", "mins", "min", "m"]):
      amount_seconds_mute = int(time) * 60
    elif any(unit in original_time for unit in ["hours", "hour", "hrs", "hr", "h"]):
      amount_seconds_mute = int(time) * 60 * 60
    elif any(unit in original_time for unit in ["days", "day", "d"]):
      amount_seconds_mute = int(time) * 60 * 60 * 24
    elif any(unit in original_time for unit in ["weeks", "week", "w"]):
      amount_seconds_mute = int(time) * 60 * 60 * 24 * 7
    elif any(unit in original_time for unit in ["months", "month", "mo", "m"]):
      amount_seconds_mute = int(time) * 60 * 60 * 24 * 30

    if not reason:
      cursor.execute("INSERT INTO mutes (user_id, guild_id, time_now, time_then) VALUES (?, ?, ?, ?)", (member.id, ctx.guild.id, int(time_module.time()), int(time_module.time()) + amount_seconds_mute))

      reason = "No reason provided."
    else:
      cursor.execute("INSERT INTO mutes (user_id, guild_id, time_now, time_then, reason) VALUES (?, ?, ?, ?, ?)", (member.id, ctx.guild.id, int(time_module.time()), int(time_module.time()) + amount_seconds_mute, reason))

    database.commit()


    # target_id TEXT, target_name TEXT, executor_id TEXT NOT NULL, executor_name TEXT NOT NULL, executor_profile_picture_url TEXT NOT NULL, executor_role TEXT NOT NULL, guild_id TEXT NOT NULL, guild_name TEXT NOT NULL, action TEXT NOT NULL, timestamp INTEGER NOT NULL, reason TEXT DEFAULT 'No reason provided.'

    if reason is None:
      cursor.execute("INSERT INTO mod_command_history (target_id, target_name, executor_id, executor_name, executor_profile_picture_url, executor_role, guild_id, guild_name, action, additional_info, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (member.id, member.name, ctx.author.id, ctx.author.name, ctx.author.avatar, "Moderator", ctx.guild.id, ctx.guild.name, "mute", f"Duration: {original_time}", int(time_module.time())))
    else:
      cursor.execute("INSERT INTO mod_command_history (target_id, target_name, executor_id, executor_name, executor_profile_picture_url, executor_role, guild_id, guild_name, action, additional_info, timestamp, reason) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (str(member.id), str(member.name), str(ctx.author.id), str(ctx.author.name), str(ctx.author.avatar), "Moderator", str(ctx.guild.id), str(ctx.guild.name), "mute", f"Duration: {original_time}", int(time_module.time()), reason))

    database.commit()

    embed = guilded.Embed(
      title = f"✅ {member.mention} has been muted!",
      description = f"Duration: {original_time}\nReason: {reason}",
      color = guilded.Color.green()
    )
    embed.set_footer(text = f"Muted ID: {member.id} | Guild ID: {ctx.guild.id}")

    await ctx.reply(embed = embed, private = False)


def setup(client):
  client.add_cog(MuteCog(client))