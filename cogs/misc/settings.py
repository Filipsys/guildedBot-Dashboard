import guilded
import asyncio

from guilded.ext import tasks, commands
from data.database.sqlite import *
from data.misc.charsAndEmojis import *
from data.misc.setting_embed_function import *


class SettingsCog(commands.Cog):
  """The 'settings' cog."""

  def __init__(self, client):
    self.client = client

  @commands.command(aliases = ["setting", "config", "configs", "configuration", "configurations", "options", "option"])
  async def settings(self, ctx):
    """View or change the bot's settings."""

    # on_setting_emoji = ":active:"
    # off_setting_emoji = ":unactive:"
    # on_setting_emoji = ":on_block:"
    # off_setting_emoji = ":off_block:"

    # filters_dict = {
    #   "guilded_invite_checker": "INVITE_CHECKER",
    #   "caps_checker": "CAPS_CHECKER",
    #   "link_checker": "LINK_CHECKER",
    #   "spam_checker": "SPAM_CHECKER",
    #   "emoji_spam_checker": "EMOJI_SPAM_CHECKER",
    #   "mass_mention_checker": "MASS_MENTION_CHECKER"
    # }

    # values_dict = {
    #   "enable": "ENABLED",
    #   "enabled": "ENABLED",
    #   "on": "ENABLED",
    #   "disable": "DISABLED",
    #   "disabled": "DISABLED",
    #   "off": "DISABLED"
    # }

    # categories_dict = {
    #   "filters": [["filter", "filters", "filtering", "filtered"], filters_dict]
    # }

    embeds = await create_settings_embed(ctx)
    embed1, embed2, embed3 = embeds[0], embeds[1], embeds[2]

    settings_msg = await ctx.send(embed = embed1)
    # misc_msg = await ctx.send(embed = embed2)
    # await ctx.send(embed = embed3)

    await settings_msg.add_reaction("90002097")
    await settings_msg.add_reaction("90002093")
    await settings_msg.add_reaction("90002221")

    check_settings_msg = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("SETTINGS_MSG", ctx.guild.id)).fetchone()
    check_misc_msg = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("MISC_MSG", ctx.guild.id)).fetchone()


    if check_settings_msg is None:
      cursor.execute("INSERT INTO guild_variables (variable, value, guild_id) VALUES (?, ?, ?)", ("SETTINGS_MSG", settings_msg.id, ctx.guild.id))
      database.commit()
    else:
      cursor.execute("UPDATE guild_variables SET value = ? WHERE variable = ? AND guild_id = ?", (settings_msg.id, "SETTINGS_MSG", ctx.guild.id))
      database.commit()


    # if check_misc_msg is None:
    #   cursor.execute("INSERT INTO guild_variables (variable, value, guild_id) VALUES (?, ?, ?)", ("MISC_MSG", misc_msg.id, ctx.guild.id))
    #   database.commit()
    # else:
    #   cursor.execute("UPDATE guild_variables SET value = ? WHERE variable = ? AND guild_id = ?", (misc_msg.id, "MISC_MSG", ctx.guild.id))
    #   database.commit()    


def setup(client):
  client.add_cog(SettingsCog(client))