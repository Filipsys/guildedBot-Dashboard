import guilded
import sqlite3
import os
import random
import time
import hashlib


from guilded.ext import commands
from dotenv import load_dotenv

from checks.messagechecks import *
from data.misc.extensions import *
from data.misc.charsAndEmojis import *
from data.misc.setting_embed_function import *
from data.misc.uptime import reset_uptime
from typing import List
from guilded.http import Route


prefix = "$"

database = sqlite3.connect("data/database/database.db")
cursor = database.cursor()


def defaultTables():
  """Create the default tables."""

  cursor.execute("CREATE TABLE IF NOT EXISTS guilds (guild_id TEXT NOT NULL UNIQUE PRIMARY KEY, prefix TEXT NOT NULL DEFAULT '$')")
  cursor.execute("CREATE TABLE IF NOT EXISTS guild_variables (guild_id TEXT NOT NULL, variable TEXT NOT NULL, value TEXT NOT NULL, FOREIGN KEY (guild_id) REFERENCES guilds(guild_id))")
  # cursor.execute("CREATE TABLE IF NOT EXISTS command_history (user_name TEXT NOT NULL, user_id TEXT NOT NULL, guild_name TEXT NOT NULL, guild_id TEXT NOT NULL, command TEXT NOT NULL, time INTEGER NOT NULL)")
  cursor.execute("CREATE TABLE IF NOT EXISTS mutes (user_id TEXT NOT NULL, guild_id TEXT NOT NULL, time_now INTEGER NOT NULL, time_then INTEGER, reason TEXT DEFAULT 'No reason provided.', FOREIGN KEY (guild_id) REFERENCES guilds(guild_id))")
  cursor.execute("CREATE TABLE IF NOT EXISTS tempbans (user_id TEXT NOT NULL, guild_id TEXT NOT NULL, time_now INTEGER NOT NULL, time_then INTEGER, reason TEXT DEFAULT 'No reason provided.', FOREIGN KEY (guild_id) REFERENCES guilds(guild_id))")
  cursor.execute("CREATE TABLE IF NOT EXISTS temproles (user_id TEXT NOT NULL, guild_id TEXT NOT NULL, role_id TEXT NOT NULL, time_now INTEGER NOT NULL, time_then INTEGER, FOREIGN KEY (guild_id) REFERENCES guilds(guild_id))")
  cursor.execute("CREATE TABLE IF NOT EXISTS warns (user_id TEXT NOT NULL, guild_id TEXT NOT NULL, amount INTEGER DEFAULT 1, reasons TEXT DEFAULT 'No reason provided.', FOREIGN KEY (guild_id) REFERENCES guilds(guild_id))")
  cursor.execute("CREATE TABLE IF NOT EXISTS user_notes (user_id TEXT NOT NULL, guild_id TEXT NOT NULL, note TEXT NOT NULL, FOREIGN KEY (guild_id) REFERENCES guilds(guild_id))")
  cursor.execute("CREATE TABLE IF NOT EXISTS infractions (guild_id TEXT NOT NULL, event TEXT NOT NULL, amount_infractions_needed INTEGER NOT NULL, action TEXT NOT NULL, duration INTEGER, FOREIGN KEY (guild_id) REFERENCES guilds(guild_id))")
  cursor.execute(f"CREATE TABLE IF NOT EXISTS connect_codes (guild_id TEXT NOT NULL, code TEXT NOT NULL, timestamp_epoch INTEGER NOT NULL, expired BOOL NOT NULL DEFAULT 0, FOREIGN KEY (guild_id) REFERENCES guilds(guild_id))")
  cursor.execute("CREATE TABLE IF NOT EXISTS mod_command_history (target_id TEXT, target_name TEXT, executor_id TEXT NOT NULL, executor_name TEXT NOT NULL, executor_profile_picture_url TEXT NOT NULL, executor_role TEXT NOT NULL, guild_id TEXT NOT NULL, guild_name TEXT NOT NULL, action TEXT NOT NULL, additional_info TEXT, timestamp INTEGER NOT NULL, reason TEXT DEFAULT 'No reason provided.', FOREIGN KEY (guild_id) REFERENCES guilds(guild_id))")
  
  cursor.execute("CREATE TABLE IF NOT EXISTS latest_bot_updates_dashboard (update_id INTEGER PRIMARY KEY AUTOINCREMENT, update_title TEXT NOT NULL, update_description TEXT NOT NULL, update_date INTEGER NOT NULL)")
  cursor.execute("CREATE TABLE IF NOT EXISTS main_server_data_dashboard (guild_id TEXT NOT NULL PRIMARY KEY, server_name TEXT NOT NULL, server_description TEXT NOT NULL, server_members INTEGER NOT NULL, category_count INTEGER NOT NULL, text_channel_count INTEGER NOT NULL, voice_channel_count INTEGER NOT NULL, role_count INTEGER NOT NULL, server_owner TEXT NOT NULL, server_owner_id TEXT NOT NULL, server_icon TEXT NOT NULL, member_count INTEGER NOT NULL, messages_sent INTEGER NOT NULL DEFAULT 0, messages_sent_timestamp TEXT NOT NULL, messages_edited INTEGER NOT NULL DEFAULT 0, messages_edited_timestamp TEXT NOT NULL, messages_deleted INTEGER NOT NULL DEFAULT 0, messages_deleted_timestamp TEXT NOT NULL, mod_cmds_ran INTEGER NOT NULL DEFAULT 0, mod_cmds_ran_timestamp TEXT NOT NULL, FOREIGN KEY (guild_id) REFERENCES guilds(guild_id))")
  cursor.execute("CREATE TABLE IF NOT EXISTS bot_info_dashboard (variable TEXT NOT NULL, value TEXT NOT NULL)")

  database.commit()



async def fetch_channels(server: guilded.Server, client: guilded.Client | commands.Bot) -> List[guilded.abc.ServerChannel]:
    """|coro|

    Fetch the list of channels in a server.

    Returns
    --------
    List[:class:`ServerChannel`]
        The channels of the server.
    """
    data = await client.http.request(Route('GET', f'/teams/{server.id}/channels', override_base=Route.USER_BASE))

    channels = []
    for channel in data["channels"]:
        channel["serverId"] = channel["teamId"]
        channel_object = client.http.create_channel(data=channel)
        channels.append(channel_object)
        client.http.add_to_server_channel_cache(channel_object)
    return channels



class GuildedBot(commands.Bot):
  """The bot class."""

  def __init__(self):
    """Initialize the bot class.""" 

    super().__init__(command_prefix = commands.when_mentioned_or(prefix), case_insensitive = True, features = guilded.ClientFeatures(official_markdown = True))


  # -----------------------------------------------


  async def setup_hook(self) -> None:
    """The setup hook."""
    self.remove_command("help")

    for extensions in extension_groups:
      for extension in extensions:
        client.load_extension(extension)


  # -----------------------------------------------


  async def on_ready(self):
    """When the bot is ready."""

    defaultTables()

    print("------------------------------------")
    print(f"Bot Name: {client.user.name}")
    print(f"Guilded.py Version: {guilded.__version__}")
    print(f"Bot ID: {client.user.id}")
    print("------------------------------------")

    # reset_uptime()

    check_empty = cursor.execute("SELECT value FROM bot_info_dashboard WHERE variable = 'STARTUP_TIMESTAMP_EPOCH'").fetchone()

    if check_empty is None:
      cursor.execute("INSERT INTO bot_info_dashboard (variable, value) VALUES ('STARTUP_TIMESTAMP_EPOCH', ?)", (str(datetime.datetime.now().timestamp()),))
    else:
      cursor.execute("UPDATE bot_info_dashboard SET value = ? WHERE variable = 'STARTUP_TIMESTAMP_EPOCH'", (str(datetime.datetime.now().timestamp()),))

    database.commit()


    print("Uptime set")
    print("------------------------------------")


# ----------------------------------------------- START THE BOT -----------------------------------------------


client = GuildedBot()


@client.event
async def on_message(message):
  # if message.author.bot:
  #   return
  
  if message.content == f"@{client.user.name}":
    await message.channel.send(f"Hello! I am a bot. Use `{prefix}help` to see my commands.")
  

  CHECKING_DICT = {
    "INVITE_CHECKER": check_guilded_invite,
    "CAPS_CHECKER": check_caps,
    "LINK_CHECKER": check_links,
    "SAFE_BROWSING_CHECKER": check_unsafe_links,
    "NSFW_IMAGE_CHECKER": check_nsfw_image,
    "SPAM_CHECKER": check_spam,
    "EMOJI_SPAM_CHECKER": check_emoji_spam,
    "MASS_MENTION_CHECKER": check_mass_mentions,
    "NEW_ACCOUNT_CHECKER": check_new_account
  }

  for item in CHECKING_DICT:
    check_variable_exists = cursor.execute("SELECT variable, value FROM guild_variables WHERE variable = ? AND guild_id = ?", (item, message.guild.id)).fetchone()

    if check_variable_exists is not None and check_variable_exists[1] == "ENABLED":
      await CHECKING_DICT[item](message)
      
  await client.process_commands(message)


@client.event
async def on_message_reaction_add(reaction):
  """The on_reaction_add event listener."""
  if reaction.user.bot:
    return
  
  if reaction.message.guild.owner_id != reaction.user.id:
    return await reaction.message.remove_reaction(reaction.emoji, reaction.user)

  if reaction.message.guild is None:
    return


  embeds = await create_settings_embed(reaction.message)
  embed1, embed2, info_embed = embeds[0], embeds[1], embeds[2]

  page_number = 1
  PAGE_DICT = {
    1: embed1,
    2: embed2,
  }

  async def check_page_number_and_edit(reaction, reaction_emoji_id: int, page_number: int):
    if reaction_emoji_id == 90002097:
      page_number -= 1
    elif reaction_emoji_id == 90002093:
      page_number += 1

    if page_number == 0:
      if reaction_emoji_id == 90002097:
        page_number = 1
      elif reaction_emoji_id == 90002093:
        page_number = PAGE_DICT.__len__()

    await reaction.message.remove_reaction(reaction.emoji, reaction.user)
    await reaction.message.edit(embed = PAGE_DICT[page_number].set_footer(icon_url = "https://cdn.gilcdn.com/ContentMediaGenericFiles/559b3174c1a674b785165d2ea853fdb8-Full.webp", text = f"Page {page_number}/{PAGE_DICT.__len__()} // Need help? Use the $help command."))


  if reaction.emoji.id == 90002097:
    await check_page_number_and_edit(reaction, reaction.emoji.id, page_number)
  elif reaction.emoji.id == 90002093:
    await check_page_number_and_edit(reaction, reaction.emoji.id, page_number)

  elif reaction.emoji.id == 90002221:
    page_number = 0

    await reaction.message.remove_reaction(reaction.emoji, reaction.user)
    await reaction.message.edit(embed = info_embed)  



# error control

@client.event
async def on_command_error(ctx, error):

  errors_dict = {
    commands.MissingRequiredArgument: "You are missing a required argument.",
    commands.MissingPermissions: "You are missing the required permissions to run this command.",
    commands.BotMissingPermissions: "I am missing the required permissions to run this command.",
    commands.CommandNotFound: "This command does not exist.",
    commands.CommandOnCooldown: "This command is on cooldown. Please try again in {error.retry_after:.2f} seconds.",
    commands.CheckFailure: "You do not have permission to run this command.",
    commands.BadArgument: "You provided a bad argument.",
    commands.MissingRole: "You are missing the required role to run this command."
  }

  if type(error) in errors_dict:
    return await ctx.send(errors_dict[type(error)])

  raise error

# ===============================================

@client.event
async def on_message_edit(message_before, message_after):
  prefix = "$"
  keywords = ["setting", "config", "configs", "configuration", "configurations", "options", "option"]
  keywords_2 = ["change"]


  VALUES_DICT = {
    "enable": "ENABLED",
    "enabled": "ENABLED",
    "on": "ENABLED",
    "yes": "ENABLED",
    "y": "ENABLED",
    "disable": "DISABLED",
    "disabled": "DISABLED",
    "off": "DISABLED",
    "no": "DISABLED",
    "n": "DISABLED"
  }

  CATEGORIES_DICT = {
    "permissions": [["permission", "permissions", "perms", "perm"], PERMISSIONS_DICT],
    "filters": [["filter", "filters", "filtering", "filtered"], FILTERS_DICT],
    "miscellaneous": [["misc", "miscellaneous", "other", "etc"], MISCELLANEOUS_DICT],
  }



  if message_before.author.bot:
    return
  
  if message_after.author.guild_permissions.administrator != True:
    if any(keyword in message_after.content for keyword in keywords) and message_after.content.startswith(prefix):
      return await message_after.channel.send("You don't have permission to use this command.", delete_after = 10)
    
  if any(keyword in message_after.content for keyword in keywords) and message_after.content.startswith(prefix):
    setings_msg = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("SETTINGS_MSG", message_after.guild.id)).fetchone()
    misc_msg = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("MISC_MSG", message_after.guild.id)).fetchone()

    cmd_setting = None
    if "change" in message_after.content:
      cmd_setting = "change"


    # Quick check to see if the settings message exists

    try:
      settings_msg = await message_after.channel.fetch_message(setings_msg[0])
    except:
      embeds = await create_settings_embed(message_after)

      settings_msg = await message_after.channel.send(embed = embeds[0])

    try:
      misc_msg = await message_after.channel.fetch_message(misc_msg[0])
    except:
      embeds = await create_settings_embed(message_after)

      misc_msg = await message_after.channel.send(embed = embeds[1])

    # Check for keywords

    try:
      list_of_words = message_after.content.split()

      option = list_of_words[1]
      value = list_of_words[-1]
      
      if len(list_of_words) > 3:
        variable = " ".join(list_of_words[2:-1])
      else:
        variable = list_of_words[2]

    except:
      embed = guilded.Embed(
        title = "⚠️ Error",
        description = "Invalid syntax. Please use the following syntax: `$setting <option> <variable> <value>`",
        color = guilded.Color.red()
      )

      return await message_after.channel.send(embed = embed)
    

    def check_if_variable_exists_in_abbreviations_dict(variable):
      for item in ABBREVIATIONS_DICT:
        if variable in ABBREVIATIONS_DICT[item]:
          return item
      return None
    
    
    if cmd_setting == "change":
      if list_of_words[-2].lower() == "muted_role" or list_of_words[-2].lower() == "mutedrole":
        try:
          muted_role_id = int(value)
        except:
          embed = guilded.Embed(
            title = "⚠️ Error",
            description = "The muted role ID must be an integer.",
            color = guilded.Color.red()
          )

          return await message_after.channel.send(embed = embed)
        

        roles = await guilded.Server.fetch_roles(message_after.guild)
        found_muted_role = None

        for role in roles:
          if role.id == muted_role_id:
            found_muted_role = role
            break

        if not found_muted_role:
          embed = guilded.Embed(
            title = "⚠️ Error",
            description = "The muted role was not found on the server. Please make sure the muted role ID is correct.",
            color = guilded.Color.red()
          )

          return await message_after.channel.send(embed = embed)

        
        check_variable_exists = cursor.execute("SELECT variable FROM guild_variables WHERE variable = ? AND guild_id = ?", ("MUTED_ROLE", message_after.guild.id)).fetchone()

        if check_variable_exists is not None:
          cursor.execute("UPDATE guild_variables SET value = ? WHERE variable = ? AND guild_id = ?", (muted_role_id, "MUTED_ROLE", message_after.guild.id))
          database.commit()
          
          embed = guilded.Embed(
            title = "✅ Success",
            description = "Muted role has been updated.",
            color = guilded.Color.green()
          )

          return await message_after.channel.send(embed = embed)
        

        cursor.execute("INSERT INTO guild_variables (variable, value, guild_id) VALUES (?, ?, ?)", ("MUTED_ROLE", muted_role_id, message_after.guild.id))
        database.commit()

        embed = guilded.Embed(
          title = "✅ Success",
          description = "Muted role has been set.",
          color = guilded.Color.green()
        )

        return await message_after.channel.send(embed = embed)

    
    if check_if_variable_exists_in_abbreviations_dict(variable) is not None:
      variable = check_if_variable_exists_in_abbreviations_dict(variable)


    async def check_option(c_dict):
      check_variable_exists = cursor.execute("SELECT variable FROM guild_variables WHERE variable = ? AND guild_id = ?", (c_dict, message_after.guild.id)).fetchone()

      if check_variable_exists is not None:
        cursor.execute("UPDATE guild_variables SET value = ? WHERE variable = ? AND guild_id = ?", (VALUES_DICT[value], c_dict, message_after.guild.id))
        database.commit()

        embeds = await create_settings_embed(message_after)

        await settings_msg.edit(embed = embeds[0])
        await misc_msg.edit(embed = embeds[1])
        return
      
      cursor.execute("INSERT INTO guild_variables (variable, value, guild_id) VALUES (?, ?, ?)", (c_dict, VALUES_DICT[value], message_after.guild.id))
      database.commit()

      embeds = await create_settings_embed(message_after)

      await settings_msg.edit(embed = embeds[0])
      await misc_msg.edit(embed = embeds[1])

    for category in CATEGORIES_DICT:
      if option.lower() in CATEGORIES_DICT[category][0]:
        await check_option(CATEGORIES_DICT[category][1][variable])


async def addChannelsIntoDB(ctx):
  temp_string = ""
  channels = await fetch_channels(ctx.server, ctx.bot)

  for channel in channels:
    temp_string += f"{channel.id}:::{channel.name},,,"


  check_all_channels = cursor.execute("SELECT value FROM guild_variables WHERE variable = 'ALL_CHANNELS' AND guild_id = ?", (ctx.guild.id,)).fetchone()

  if check_all_channels is not None:
    cursor.execute("UPDATE guild_variables SET value = ? WHERE variable = 'ALL_CHANNELS' AND guild_id = ?", (temp_string, ctx.guild.id))
  else:
    cursor.execute("INSERT INTO guild_variables (guild_id, variable, value) VALUES (?, 'ALL_CHANNELS', ?)", (ctx.guild.id, temp_string))

  database.commit()


@client.command(aliases = ["connect", "connectserver", "connect_server"])
async def connect(ctx):
  """Gives a one-time use code to connect the server bot to the website."""

  check_code_exists = cursor.execute("SELECT code FROM connect_codes WHERE guild_id = ?", (ctx.guild.id,)).fetchone()

  if check_code_exists is not None:
    return await ctx.reply("You already have a code. Please use that one.", private = True)
  
  random_code = random.randint(100000, 999999)
  hashed_code = hashlib.sha256(str(random_code).encode()).hexdigest()

  check_duplicate_code = cursor.execute("SELECT code FROM connect_codes WHERE code = ?", (hashed_code,)).fetchone()

  while check_duplicate_code is not None:
    random_code = random.randint(100000, 999999)
    hashed_code = hashlib.sha256(str(random_code).encode()).hexdigest()

    check_duplicate_code = cursor.execute("SELECT code FROM connect_codes WHERE code = ?", (hashed_code,)).fetchone()

  cursor.execute("INSERT INTO connect_codes (guild_id, timestamp_epoch, code) VALUES (?, ?, ?)", (ctx.guild.id, int(time.time()), hashed_code))

  
  await addChannelsIntoDB(ctx)
  await ctx.send(f"One-time use code: `{random_code}`")



@client.command(aliases = ["expirecode", "expire_code"])
async def expire(ctx):
  """Expires the current code."""

  check_code_exists = cursor.execute("SELECT code, expired FROM connect_codes WHERE guild_id = ?", (ctx.guild.id,)).fetchone()

  if check_code_exists is None:
    return await ctx.reply("You don't have a code to expire.", private = True)
  
  if check_code_exists[1] == 1:
    return await ctx.reply("Code has already been expired.", private = True)

  cursor.execute("UPDATE connect_codes SET expired = 1 WHERE guild_id = ?", (ctx.guild.id,))
  database.commit()

  await ctx.reply("Code has been expired.", private = True)


@client.command(aliases = ["resetcode", "reset_code"])
async def code_reset(ctx):
  """Resets the code."""

  time.sleep(1)

  check_code_exists = cursor.execute("SELECT code FROM connect_codes WHERE guild_id = ?", (ctx.guild.id,)).fetchone()

  if check_code_exists is None:
    return await ctx.reply("You don't have a code to reset.", private = True)
  

  random_code = random.randint(100000, 999999)
  hashed_code = hashlib.sha256(str(random_code).encode()).hexdigest()

  cursor.execute("DELETE FROM connect_codes WHERE guild_id = ?", (ctx.guild.id,))
  cursor.execute("INSERT INTO connect_codes (guild_id, timestamp_epoch, code) VALUES (?, ?, ?)", (ctx.guild.id, int(time.time()), hashed_code))
  database.commit()

  await addChannelsIntoDB(ctx)
  await ctx.reply(f"Code has been reset. New code: `{random_code}`", private = True)


@client.command()
async def testping(ctx):
  await ctx.send(ctx.author.mention)


if __name__ == "__main__":
  """Run the bot."""

  load_dotenv(dotenv_path = "data/secrets/secrets.env")
  client.run(os.getenv('DISCORD_TOKEN'))



  





# @client.command()
# async def rules(ctx):
#   rules = """
# **1. Follow the Guilded TOS**
# -⠀[https://guilded.gg/terms](https://guilded.gg/terms)
# -⠀[https://guilded.gg/guidelines](https://support.guilded.gg/hc/en-us/articles/360052815873-Community-Guidelines)

# **2. Be respectful with all members**
# -⠀Be respectful to others, no death threats,
# -⠀sexism, hate speech, racism.
# -⠀No doxxing, swatting, witch hunting.

# **3. No Advertising**
# -⠀Includes DM Advertising. We do not allow advertising
# -⠀here of any kind.

# **4. No NSFW content**
# -⠀Anything involving gore or sexual content is not allowed.
# -⠀NSFW = Not Safe for Work

# **5. No spamming in text or VC**
# -⠀Do not spam messages, soundboards, voice changers,
# -⠀or earrape in any channel.

# **6. No malicious content**
# -⠀No grabify links, viruses, crash videos, links to viruses,
# -⠀or token grabbers. These will result in an automated ban.

# **7. Do not DM the staff team **
# -⠀Please open a ticket instead of DMing staff members.

# **8. Profile Picture / Banner Rules**
# -⠀No NSFW allowed
# -⠀No racism
# -⠀No brightly flashing pictures to induce an epileptic attack.

# **9. Emoji Rules**
# -⠀No NSFW allowed
# -⠀No racism
# -⠀No brightly flashing pictures to induce an epileptic attack.

# **10. Use English only**
# -⠀We cannot easily moderate chats in different languages, sorry. English only."""

#   embed = guilded.Embed(
#     title = "📃 **Rules!**",
#     description = rules,
#     color = guilded.Color.green()
#   )

#   await ctx.send(embed = embed)