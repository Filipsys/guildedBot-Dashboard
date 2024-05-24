import guilded
import time as time_module

from guilded.ext import commands
from data.database.sqlite import *


class TempbanCog(commands.Cog):
  """The 'tempban' cog."""

  def __init__(self, client):
    self.client = client

  @commands.command()
  async def tempban(self, ctx, m, time: str, reason: str = None):
    """The 'tempban' command."""

    check_guild_exists = cursor.execute("SELECT guild_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,)).fetchone()
    if check_guild_exists is None:
      return await ctx.send("Please run the `$start` command first.")

    member = await commands.MemberConverter().convert(ctx, str(m).replace("@", ""))

    original_time = time
    if any(unit in time for unit in ["hours", "hour", "hrs", "hr", "h"]):
      time = time.replace("hours", "").replace("hour", "").replace("hrs", "").replace("hr", "").replace("h", "")
    elif any(unit in time for unit in ["days", "day", "d"]):
      time = time.replace("days", "").replace("day", "").replace("d", "")
    elif any(unit in time for unit in ["weeks", "week", "w"]):
      time = time.replace("weeks", "").replace("week", "").replace("w", "")
    elif any(unit in time for unit in ["months", "month", "mo", "m"]):
      time = time.replace("months", "").replace("month", "").replace("mo", "").replace("m", "")
    elif any(unit in time for unit in ["years", "year", "y"]):
      time = time.replace("years", "").replace("year", "").replace("y", "")

    await member.ban()

    amount_seconds_tempban = 0
    if any(unit in original_time for unit in ["hours", "hour", "hrs", "hr", "h"]):
      amount_seconds_tempban = int(time) * 60 * 60
    elif any(unit in original_time for unit in ["days", "day", "d"]):
      amount_seconds_tempban = int(time) * 60 * 60 * 24
    elif any(unit in original_time for unit in ["weeks", "week", "w"]):
      amount_seconds_tempban = int(time) * 60 * 60 * 24 * 7
    elif any(unit in original_time for unit in ["months", "month", "mo", "m"]):
      amount_seconds_tempban = int(time) * 60 * 60 * 24 * 30
    elif any(unit in original_time for unit in ["years", "year", "y"]):
      amount_seconds_tempban = int(time) * 60 * 60 * 24 * 365

    if not reason:
      cursor.execute("INSERT INTO tempbans (user_id, guild_id, time_now, time_then) VALUES (?, ?, ?, ?)", (member.id, ctx.guild.id, int(time_module.time()), int(time_module.time()) + int(time)))

      reason = "No reason provided."
    else:
      cursor.execute("INSERT INTO mutes (user_id, guild_id, time_now, time_then, reason) VALUES (?, ?, ?, ?, ?)", (member.id, ctx.guild.id, int(time_module.time()), int(time_module.time()) + amount_seconds_tempban, reason))

    database.commit()

    embed = guilded.Embed(
      title = f"✅ {member.mention} has been tempbanned!",
      description = f"Duration: {original_time}\nReason: {reason}",
      color = guilded.Color.green()
    )
    embed.set_footer(text = f"Muted ID: {member.id} | Guild ID: {ctx.guild.id}")

    await ctx.reply(embed = embed, private = True)


def setup(client):
  client.add_cog(TempbanCog(client))