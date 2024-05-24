import guilded
import datetime

from guilded.ext import commands
from data.misc.charsAndEmojis import *
from data.database.sqlite import *


on_setting_emoji = ":on_block:"
off_setting_emoji = ":off_block:"

PERMISSIONS_DICT = {
  "admin_immunity": "ADMIN_IMMUNITY",
  "inherit_guilded_permissions": "INHERIT_GUILDED_PERMISSIONS",
}

FILTERS_DICT = {
  "guilded_invite_checker": "INVITE_CHECKER",
  "caps_checker": "CAPS_CHECKER",
  "link_checker": "LINK_CHECKER",
  "safe_browsing_checker": "SAFE_BROWSING_CHECKER",
  "nsfw_image_checker": "NSFW_IMAGE_CHECKER",
  "spam_checker": "SPAM_CHECKER",
  "emoji_spam_checker": "EMOJI_SPAM_CHECKER",
  "mass_mention_checker": "MASS_MENTION_CHECKER",
  "new_account_checker": "NEW_ACCOUNT_CHECKER",
}

MISCELLANEOUS_DICT = {
  "advanced_customisation": "ADVANCED_CUSTOMISATION",
  "infraction_customisation": "INFRACTION_CUSTOMISATION",
}


# ADVANCED_SETTINGS_INFO = {
#   "Admin Immunity": [],
#   "Inherit Guilded Permissions": [],
#   "Guilded Invite Checker": [],
#   "Caps Checker": ["", f"\n{EMPTY_CHARACTER * 2}:right-gray-line: Threshold for message filter: **90%**"],
#   "Link Checker": [],
#   "Safe Browsing Checker": [],
#   "Spam Checker": ["", f"\n{EMPTY_CHARACTER * 2}:right-gray-line: Threshold for message count filter: **5**"],
#   "Emoji Spam Checker": ["", f"\n{EMPTY_CHARACTER * 2}:right-gray-line: Threshold for emoji count filter: **10**"],
#   "Mass Mention Checker": ["", f"\n{EMPTY_CHARACTER * 2}:right-gray-line: Mention threshold: **5**"],
#   "New Account Checker": ["", f"\n{EMPTY_CHARACTER * 2}:right-gray-line: Threshold for account age filter: **7 days**"],
#   "Infraction Customization": [],
#   "Advanced Customization": [],
# }

ADVANCED_SETTINGS_INFO = {
  "admin_immunity": [],
  "inherit_guilded_permissions": [],
  "guilded_invite_checker": [],
  "caps_checker": ["", f"\n{EMPTY_CHARACTER * 2}:right-gray-line: Threshold for message filter: **90%**"],
  "link_checker": [],
  "safe_browsing_checker": [],
  "nsfw_image_checker": [],
  "spam_checker": ["", f"\n{EMPTY_CHARACTER * 2}:right-gray-line: Threshold for message count filter: **5**"],
  "emoji_spam_checker": ["", f"\n{EMPTY_CHARACTER * 2}:right-gray-line: Threshold for emoji count filter: **10**"],
  "mass_mention_checker": ["", f"\n{EMPTY_CHARACTER * 2}:right-gray-line: Mention threshold: **5**"],
  "new_account_checker": ["", f"\n{EMPTY_CHARACTER * 2}:right-gray-line: Threshold for account age filter: **7 days**"],
  "infraction_customisation": [],
  "advanced_customisation": [],
}


INFRACTION_SETTINGS_OPTIONS = {
  "admin_immunity": False,
  "inherit_guilded_permissions": False,
  "guilded_invite_checker": True,
  "caps_checker": True,
  "link_checker": True,
  "safe_browsing_checker": True,
  "nsfw_image_checker": True,
  "spam_checker": True,
  "emoji_spam_checker": True,
  "mass_mention_checker": True,
  "new_account_checker": False,
  "infraction_customisation": False,
  "advanced_customisation": False,
}

ABBREVIATIONS_DICT = {
  "admin_immunity": ["admin_immunity", "adminimmunity", "admin-immunity", "immunity", "admin", "admin immunity"],
  "inherit_guilded_permissions": ["inherit_guilded_permissions", "inheritguildedpermissions", "inherit-guilded-permissions", "inherit-permissions", "inherit_permissions", "inheritpermissions", "inherit guilded permissions", "inherit permissions"],
  "guilded_invite_checker": ["guilded_invite_checker", "guildedinvitechecker", "guilded-invite-checker", "guilded_invite_detection", "guildedinvitedetection", "guilded-invite-detection", "guilded invite checker", "guilded invite detection"],
  "caps_checker": ["caps_checker", "capschecker", "caps-checker", "caps detection", "capsdetection"],
  "link_checker": ["link_checker", "linkchecker", "link-checker", "link detection", "linkdetection"],
  "safe_browsing_checker": ["safe_browsing_checker", "safebrowsingchecker", "safe-browsing-checker", "safe browsing detection", "safebrowsingdetection", "safe-browsing-detection", "safe browsing checker"],
  "nsfw_image_checker": ["nsfw_image_checker", "nsfwimagechecker", "nsfw-image-checker", "nsfw image detection", "nsfwimagedetection", "nsfw-image-detection", "nsfw image checker", "nsfw detection", "nsfwdetection", "nsfw_checker", "nsfwchecker", "nsfw-checker"],
  "spam_checker": ["spam_checker", "spamchecker", "spam-checker", "spam detection", "spamdetection"],
  "emoji_spam_checker": ["emoji_spam_checker", "emojispamchecker", "emoji-spam-checker", "emoji spam detection", "emojispamdetection", "emoji-spam-detection", "emoji spam checker"],
  "mass_mention_checker": ["mass_mention_checker", "massmentionchecker", "mass-mention-checker", "mass mention detection", "massmentiondetection", "mass-mention-detection", "mass mention checker"],
  "new_account_checker": ["new_account_checker", "newaccountchecker", "new-account-checker", "new account detection", "newaccountdetection", "new-account-detection", "new account checker"],
  "infraction_customisation": ["infraction_customisation", "infractioncustomisation", "infraction-customisation", "infraction customisation", "infractioncustomization", "infraction-customization", "infraction customisation"],
  "advanced_customisation": ["advanced_customisation", "advancedcustomisation", "advanced-customisation", "advanced customisation", "advancedcustomization", "advanced-customization", "advanced customisation"]
}


# infraction_text = f"\n{EMPTY_CHARACTER * 2}:smalldot: **Infraction settings**\n{EMPTY_CHARACTER * 6}`[input1]` :view-as-role-arrow: `[input2]`\n{EMPTY_CHARACTER * 6}`[input3]` :view-as-role-arrow: `[input4]`\n{EMPTY_CHARACTER * 6}`[input5]` :view-as-role-arrow: `[input6]`\n\n{EMPTY_CHARACTER * 5}Custom infraction slots available: **[input7]**\n"
# infraction_text = f"\n{EMPTY_CHARACTER * 2}:smalldot: **Infraction settings**\n{EMPTY_CHARACTER * 6}`[input1]` :view-as-role-arrow: `[input2]`\n\n{EMPTY_CHARACTER * 5}Custom infraction slots available: **[input7]**\n"

infraction_text = f"**Infraction events**\n{EMPTY_CHARACTER}`[input1]` :view-as-role-arrow: `[input2]`\n{EMPTY_CHARACTER}`[input3]` :view-as-role-arrow: `[input4]`\n{EMPTY_CHARACTER}`[input5]` :view-as-role-arrow: `[input6]`\n{EMPTY_CHARACTER}`[input7]` :view-as-role-arrow: `[input8]`\n{EMPTY_CHARACTER}`[input9]` :view-as-role-arrow: `[input10]`\n\n{EMPTY_CHARACTER}Custom infraction slots available: **[input7]**"

# LOGGING_STYLES = {
#   "cozy": {"title": "<user> <action> <location>", "description": "<detailed-action> <location> <user> <content> <reason>"},
#   "compact": {"title": "<user> <action>", "description": "<detailed-action> <location> <user> <content> <reason>"},
#   "complex": {"title": "<user> <action> <location>", "description": "<detailed-action> <location> <user> <content> <reason>\n**Additional information**\n**Timestamp:** <timestamp>\n**Moderator:** <moderator>\n\n**Message ID:** `<message_id>`\n**Channel ID:** `<channel_id>`\n**Guild ID:** `<guild_id>`"}
# }

LOGGING_STYLES = [
  "cozy",
  "compact",
  "complex"
]

def create_logging_embed(msg, action, message = None, moderator = None, reason = None):
  """Creates a logging embed for the specified action."""

  logging_style = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("LOGGING_STYLE", msg.guild.id)).fetchone()[0]

  if not logging_style:
    cursor.execute("INSERT INTO guild_variables (guild_id, variable, value) VALUES (?, ?, ?)", (msg.guild.id, "LOGGING_STYLE", "cozy"))
    database.commit()

    logging_style = "cozy"


  _user = msg.author
  _channel = f"in #{msg.channel}"
  _timestamp = datetime.datetime.now().strftime("%H:%M.%S // %d/%m/%Y")
  _message_id = msg.id
  _guild_id = msg.guild.id
  _channel_id = msg.channel.id

  _message = " " if not message else f"```{message}```\n\n"
  moderator = "System" if not moderator else moderator
  reason = "No reason provided." if not reason else reason



  if logging_style == "cozy":
    embed_title = f":discord-eq: **{_user} {action} {_channel}**"
    embed_description = f"{_message}**Reason:** {reason}"

  elif logging_style == "compact":
    embed_title = f""
    embed_description = f":discord-eq: **{_user} {action} {_channel}**\n{_message}Reason: {reason}"

  elif logging_style == "complex":
    embed_title = f":discord-eq: {_user} {action} {_channel}"
    embed_description = f"{_message}**Reason:** {reason}\n**Timestamp:** {_timestamp}\n**Moderator:** {moderator}"


  if not embed_title:
    embed = guilded.Embed(description = embed_description, color = guilded.Color.black())
  else:
    embed = guilded.Embed(title = embed_title, description = embed_description, color = guilded.Color.black())

  if logging_style == "complex":
    embed.add_field(name = "", value = f"**Message ID:** `{_message_id}`\n**Channel ID:** `{_channel_id}`\n**Guild ID:** `{_guild_id}`", inline = False)

  return embed



async def create_settings_embed(msg):
  embed_filters_cache = {}
  advanced_custom_texts_cache = {}

  check_inherit_guilded_permissions = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("INHERIT_GUILDED_PERMISSIONS", msg.guild.id)).fetchone()
  check_adv_custom = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("ADVANCED_CUSTOMISATION", msg.guild.id)).fetchone()
  check_infraction_custom = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("INFRACTION_CUSTOMISATION", msg.guild.id)).fetchone()


  if check_adv_custom is None or check_adv_custom[0] == "DISABLED":
    for key, value in ADVANCED_SETTINGS_INFO.items():
      advanced_custom_texts_cache[key] = " "

  elif check_adv_custom[0] == "ENABLED":
    for key, value in ADVANCED_SETTINGS_INFO.items():

      if value == []:
        advanced_custom_texts_cache[key] = " "
      else:
        check_variable_exists = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", (key.upper().replace(" ", "_"), msg.guild.id)).fetchone()

        if check_variable_exists is None or check_variable_exists[0] == "DISABLED":
          advanced_custom_texts_cache[key] = " "
        elif check_variable_exists[0] == "ENABLED":
          advanced_custom_texts_cache[key] = value[1]


  # if check_infraction_custom is None or check_infraction_custom[0] == "DISABLED":
  #   advanced_custom_texts_cache['infraction_customisation'] = " "
  
  # elif check_infraction_custom[0] == "ENABLED":
  #   for key, value in ADVANCED_SETTINGS_INFO.items():
  #     if key in INFRACTION_SETTINGS_OPTIONS:
  #       if INFRACTION_SETTINGS_OPTIONS[key]:
  #         advanced_custom_texts_cache[key] = f"{infraction_text}\n"



  if check_inherit_guilded_permissions is None:
    cursor.execute("INSERT INTO guild_variables (guild_id, variable, value) VALUES (?, ?, ?)", (msg.guild.id, "INHERIT_GUILDED_PERMISSIONS", "ENABLED"))
    database.commit()
  


  for i in PERMISSIONS_DICT:
    check_variable_exists = cursor.execute("SELECT value, variable FROM guild_variables WHERE variable = ? AND guild_id = ?", (PERMISSIONS_DICT[i], msg.guild.id)).fetchone()

    if check_variable_exists is None or check_variable_exists[0] == "DISABLED":
      embed_filters_cache[i] = off_setting_emoji
    elif check_variable_exists[0] == "ENABLED":
      embed_filters_cache[i] = on_setting_emoji

  for i in FILTERS_DICT:
    check_variable_exists = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", (FILTERS_DICT[i], msg.guild.id)).fetchone()

    if check_variable_exists is None or check_variable_exists[0] == "DISABLED":
      embed_filters_cache[i] = off_setting_emoji
    elif check_variable_exists[0] == "ENABLED":
      embed_filters_cache[i] = on_setting_emoji

  for i in MISCELLANEOUS_DICT:
    check_variable_exists = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", (MISCELLANEOUS_DICT[i], msg.guild.id)).fetchone()

    if check_variable_exists is None or check_variable_exists[0] == "DISABLED":
      embed_filters_cache[i] = off_setting_emoji
    elif check_variable_exists[0] == "ENABLED":
      embed_filters_cache[i] = on_setting_emoji



  logging_channel = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("LOGS_CHANNEL", msg.guild.id)).fetchone()

  if not logging_channel:
    log_text_string = f"No logging // ~~Default logging~~ // ~~Advanced logging~~"
  
  elif logging_channel:
    logging_channel = await msg.guild.getch_channel(logging_channel[0])

    check_adv_logging = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("ADVANCED_LOGGING", msg.guild.id)).fetchone()

    if check_adv_logging is None or check_adv_logging[0] == "DISABLED":
      log_text_string = f"~~No logging~~ // Default logging // ~~Advanced logging~~\n\n{EMPTY_CHARACTER}Logging channel: {logging_channel.name}"
    elif check_adv_logging[0] == "ENABLED":
      log_text_string = f"~~No logging~~ // ~~Default logging~~ // Advanced logging\n\n{EMPTY_CHARACTER}Logging channel: {logging_channel.name}"

  

  check_infraction_custom = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("INFRACTION_CUSTOMISATION", msg.guild.id)).fetchone()

  if check_infraction_custom is None or check_infraction_custom[0] == "DISABLED":
    infraction_text_string = " "
  
  elif check_infraction_custom[0] == "ENABLED":
    # infraction_text_string = infraction_text

    get_guild_infractions = cursor.execute("SELECT event, amount_infractions_needed, action, duration FROM infractions WHERE guild_id = ? ORDER BY duration ASC", (msg.guild.id,)).fetchall()

    if not get_guild_infractions:
      infraction_text_string = " "
    else:
      infraction_text_string = "**Infractions**\n\n"

      for i in get_guild_infractions:
        if i[3] is None:
          infraction_text_string += f":right-gray-line: `{i[0]}` :view-as-role-arrow: `{i[2]}`\n"
        else:
          easy_duration = i[3] / 60 / 60
          easy_duration = f"{int(easy_duration)} hours" if easy_duration > 1 else f"{int(easy_duration)} hour"

          infraction_text_string += f":right-gray-line: `after {i[1]} {i[0]}` :view-as-role-arrow: `{i[2]} for {easy_duration}`\n"

      infraction_text_string += f"\n{EMPTY_CHARACTER}Custom infraction slots available: **{10 - len(get_guild_infractions)}**"



  embed = guilded.Embed(
    title = f":moderator: Simple Moderation settings {TOPBLUEBETA_EMOJI}",
    description = f"**Permissions** {TOPREDSOON_EMOJI}\n{embed_filters_cache['admin_immunity']} Admin immunity {TOPREDSOON_EMOJI}{advanced_custom_texts_cache['admin_immunity']}\n{embed_filters_cache['inherit_guilded_permissions']} Inherit Guilded permissions{advanced_custom_texts_cache['inherit_guilded_permissions']}\n\n**Logging** {TOPREDSOON_EMOJI}\n{EMPTY_CHARACTER}{log_text_string}\n\n**Filters / listeners** {TOPREDSOON_EMOJI}\n{EMPTY_CHARACTER}{embed_filters_cache['guilded_invite_checker']} Guilded invite detection{advanced_custom_texts_cache['guilded_invite_checker']}\n{EMPTY_CHARACTER}{embed_filters_cache['caps_checker']} Caps detection{advanced_custom_texts_cache['caps_checker']}\n{EMPTY_CHARACTER}{embed_filters_cache['link_checker']} Link detection{advanced_custom_texts_cache['link_checker']}\n{EMPTY_CHARACTER}{embed_filters_cache['safe_browsing_checker']} Suspicious link detection {TOPBLUEBETA_EMOJI} :view-as-role-arrow: [Learn more](https://developers.google.com/safe-browsing){advanced_custom_texts_cache['safe_browsing_checker']}\n{EMPTY_CHARACTER}{embed_filters_cache['nsfw_image_checker']} NSFW image detection {TOPREDBETA_EMOJI}{advanced_custom_texts_cache['nsfw_image_checker']}\n{EMPTY_CHARACTER}{embed_filters_cache['spam_checker']} Spam detection {TOPREDBETA_EMOJI}{advanced_custom_texts_cache['spam_checker']}\n{EMPTY_CHARACTER}{embed_filters_cache['emoji_spam_checker']} Emoji spam detection{advanced_custom_texts_cache['emoji_spam_checker']}\n{EMPTY_CHARACTER}{embed_filters_cache['mass_mention_checker']} Mass mention detection{advanced_custom_texts_cache['mass_mention_checker']}\n{EMPTY_CHARACTER}{embed_filters_cache['new_account_checker']} New account detection{advanced_custom_texts_cache['new_account_checker']}\n\n**Miscellaneous**\n{EMPTY_CHARACTER}{embed_filters_cache['advanced_customisation']}Advanced customisation {TOPREDSOON_EMOJI}{advanced_custom_texts_cache['advanced_customisation']}\n{EMPTY_CHARACTER}{embed_filters_cache['infraction_customisation']}Infraction customisation {TOPREDSOON_EMOJI}{advanced_custom_texts_cache['infraction_customisation']}",
    color = guilded.Color.green()
  )
  embed.set_footer(icon_url = "https://cdn.gilcdn.com/ContentMediaGenericFiles/559b3174c1a674b785165d2ea853fdb8-Full.webp", text = "Page 1/2 // Need help? Use the $help command.")

  seperator_embed = guilded.Embed(
    title = f"",
    description = f"{infraction_text_string}",
    color = guilded.Color.green()
  )

  second_embed = guilded.Embed(
    title = f"",
    description = f":slash-command: **To change a specific setting, edit your original message as followed:**\n```$settings -> $settings <option> <variable> <value>```\n:slash-command: **Example:**\n```$settings filter guilded_invite_checker enable```",
    color = guilded.Color.green()
  )
  second_embed.add_field(name = " ", value = f"List of options: `permission`, `filter` / `listener`, `miscellaneous`", inline = False)
  second_embed.set_footer(icon_url = "https://cdn.gilcdn.com/ContentMediaGenericFiles/559b3174c1a674b785165d2ea853fdb8-Full.webp", text = f"Need help? Use the $help command.")


  return [embed, seperator_embed, second_embed]