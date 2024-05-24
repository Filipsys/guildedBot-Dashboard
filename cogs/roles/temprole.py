import guilded
import time as time_module

from guilded.ext import commands
from data.database.sqlite import *


class TempRoleCog(commands.Cog):
  """The 'temprole' cog."""

  def __init__(self, client):
    self.client = client

  @commands.command()
  async def temprole(self, ctx, m, role_id, time: str):
    """The 'temprole' command."""

    check_guild_exists = cursor.execute("SELECT guild_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,)).fetchone()
    if check_guild_exists is None:
      return await ctx.send("Please run the `$start` command first.")

    member = await commands.MemberConverter().convert(ctx, str(m).replace("@", ""))

    role = await commands.RoleConverter().convert(ctx, role_id)

    if role not in ctx.guild.roles:
      return await ctx.send("The role you provided is not in this server.")
    

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
    else:
      return await ctx.send("Invalid time format. Please use `hours`, `days`, `weeks`, `months`, or `years`.")

    await member.add_role(role)

    amount_seconds_temprole = 0
    if any(unit in original_time for unit in ["hours", "hour", "hrs", "hr", "h"]):
      amount_seconds_temprole = int(time) * 60 * 60
    elif any(unit in original_time for unit in ["days", "day", "d"]):
      amount_seconds_temprole = int(time) * 60 * 60 * 24
    elif any(unit in original_time for unit in ["weeks", "week", "w"]):
      amount_seconds_temprole = int(time) * 60 * 60 * 24 * 7
    elif any(unit in original_time for unit in ["months", "month", "mo", "m"]):
      amount_seconds_temprole = int(time) * 60 * 60 * 24 * 30
    elif any(unit in original_time for unit in ["years", "year", "y"]):
      amount_seconds_temprole = int(time) * 60 * 60 * 24 * 365

    cursor.execute("INSERT INTO temproles (user_id, guild_id, role_id, time_now, time_then) VALUES (?, ?, ?, ?, ?)", (member.id, ctx.guild.id, role.id, int(time_module.time()), int(time_module.time()) + amount_seconds_temprole))
    database.commit()

    # embed = guilded.Embed(
    #   title = f"✅ {member.mention} has been temprolened!",
    #   description = f"Duration: {original_time}\nReason: {reason}",
    #   color = guilded.Color.green()
    # )
    embed = guilded.Embed(
      title = f"✅ {member.mention} has been given a temporary role",
      description = f"**Role:** {role.mention}\n**Duration:** {original_time}",
      color = guilded.Color.green()
    )
    embed.set_footer(text = f"Member ID: {member.id} | Guild ID: {ctx.guild.id}")

    await ctx.reply(embed = embed)


def setup(client):
  client.add_cog(TempRoleCog(client))