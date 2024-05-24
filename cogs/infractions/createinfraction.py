import guilded

from guilded.ext import commands
from data.database.sqlite import *


class CreateInfractionCog(commands.Cog):
  """The 'createinfraction' cog."""

  def __init__(self, client):
    self.client = client
  
  @commands.command(aliases = ["create_infraction", "create_infraction_event", "createinfraction"])
#   @commands.has_permissions(manage_messages = True)
  async def createinfractionevent(self, ctx, event, amount_infractions_needed, action, duration = None):
    """Create an infraction event."""

    LIST_OF_EVENTS = {
      "guilded_invite_checker": "INVITE_CHECKER",
      "caps_checker": "CAPS_CHECKER",
      "link_checker": "LINK_CHECKER",
      "safe_browsing_checker": "SAFE_BROWSING_CHECKER",
      "nsfw_image_checker": "NSFW_IMAGE_CHECKER",
      "spam_checker": "SPAM_CHECKER",
      "emoji_spam_checker": "EMOJI_SPAM_CHECKER",
      "mass_mention_checker": "MASS_MENTION_CHECKER"
    }

    LIST_OF_ACTIONS = ["kick", "ban", "mute", "addrole", "removerole", "softban", "tempban", "temprole"]


    if event not in LIST_OF_EVENTS:
      return await ctx.send("That event does not exist.")
    
    if action not in LIST_OF_ACTIONS:
      return await ctx.send("That action does not exist.")
    


    check_amount_of_infractions_on_server = cursor.execute("SELECT COUNT(guild_id) FROM infractions WHERE guild_id = ?", (ctx.guild.id,)).fetchone()

    if check_amount_of_infractions_on_server[0] >= 10:
      return await ctx.send("You cannot have more than 10 infraction events on a server.")
    

    check_infraction_event_exists = cursor.execute("SELECT event, amount_infractions_needed FROM infractions WHERE guild_id = ? AND event = ?", (ctx.guild.id, LIST_OF_EVENTS[event])).fetchone()

    if check_infraction_event_exists is not None and int(check_infraction_event_exists[1]) == int(amount_infractions_needed):
      return await ctx.send(f"An infraction event with the name `{LIST_OF_EVENTS[event]}` and the amount of infractions needed set to `{amount_infractions_needed}` already exists.")
    

    if action in ["mute", "tempban", "temprole"]:
      if duration is None:
        return await ctx.send("You must provide a duration for this action.")

      original_time = duration
      if any(unit in duration for unit in ["hours", "hour", "hrs", "hr", "h"]):
        duration = duration.replace("hours", "").replace("hour", "").replace("hrs", "").replace("hr", "").replace("h", "")
      elif any(unit in duration for unit in ["days", "day", "d"]):
        duration = duration.replace("days", "").replace("day", "").replace("d", "")
      elif any(unit in duration for unit in ["weeks", "week", "w"]):
        duration = duration.replace("weeks", "").replace("week", "").replace("w", "")
      elif any(unit in duration for unit in ["months", "month", "mo"]):
        duration = duration.replace("months", "").replace("month", "").replace("mo", "").replace("m", "")
      elif any(unit in duration for unit in ["years", "year", "y"]):
        duration = duration.replace("years", "").replace("year", "").replace("y", "")
      else:
        return await ctx.send("Invalid duration. Please provide a valid duration.")

      amount_seconds_duration = 0
      if any(unit in original_time for unit in ["hours", "hour", "hrs", "hr", "h"]):
        amount_seconds_duration = int(duration) * 60 * 60
      elif any(unit in original_time for unit in ["days", "day", "d"]):
        amount_seconds_duration = int(duration) * 60 * 60 * 24
      elif any(unit in original_time for unit in ["weeks", "week", "w"]):
        amount_seconds_duration = int(duration) * 60 * 60 * 24 * 7
      elif any(unit in original_time for unit in ["months", "month", "mo"]):
        amount_seconds_duration = int(duration) * 60 * 60 * 24 * 30
      elif any(unit in original_time for unit in ["years", "year", "y"]):
        amount_seconds_duration = int(duration) * 60 * 60 * 24 * 365


    if duration is not None:
      cursor.execute("INSERT INTO infractions (guild_id, event, amount_infractions_needed, action, duration) VALUES(?, ?, ?, ?, ?)", (ctx.guild.id, LIST_OF_EVENTS[event], amount_infractions_needed, action, amount_seconds_duration))
      database.commit()

      await ctx.send(f"Created infraction event `{LIST_OF_EVENTS[event]}` with the action `{action}` for `{duration}` and the amount of infractions needed set to `{amount_infractions_needed}`.")
    else:
      cursor.execute("INSERT INTO infractions (guild_id, event, amount_infractions_needed, action) VALUES(?, ?, ?, ?)", (ctx.guild.id, LIST_OF_EVENTS[event], amount_infractions_needed, action))
      database.commit()
    
      await ctx.send(f"Created infraction event `{LIST_OF_EVENTS[event]}` with the action `{action}` and the amount of infractions needed set to `{amount_infractions_needed}`.")

def setup(client):
  client.add_cog(CreateInfractionCog(client))