import guilded
from guilded.ext import commands

main_help_embed = guilded.Embed(
    title = "Simple Moderation bot help",
    description = "For more information on a specific command, type:\n```$help [command]```",
    color = guilded.Color.green()
    )

main_help_embed.add_field(
    name = "Simple moderation commands",
    value = "`kick`, `ban`, `unban`, `mute`, `unmute`\n\n**Advanced moderation commands**\n`addrole`, `removerole`, `messagecount`, `softban`, `tempban`, `temprole`, `notes`, `editnote`, `deletenote`, `clearnotes`",
    inline = False
    )

main_help_embed.add_field(
    name = "Miscellaneous commands",
    value = "`settings`",
    inline = False
    )


commands_text_dict = {
    "kick": ["Kick a member from the server.\n\n**Usage**\n```$kick <user> <reason (optional)>```\n\n**Example**\n```$kick @Kelly Spamming and annoying others.```", "**Remember:** `<user>` can be a mention or a user ID."],
    "ban": ["Ban a member from the server.\n\n**Usage**\n```$ban <user> <reason (optional)>```\n\n**Example**\n```$ban @Neil Phishing links are not allowed.```", "**Remember:** `<user>` can be a mention or a user ID."],
    "unban": ["Unban a member from the server.\n\n**Usage**\n```$unban <user>```\n\n**Example**\n```$unban XXXXXXXX```", "**Remember:** `<user>` can only be a user ID."],
    "mute": ["Mute a member in the server.\n\n**Usage**\n```$mute <user> [duration] <reason (optional)>```\n```$mute @Timmy 7days Sending spam in general.```", "**Remember:** `<user>` can be a mention or a user ID. `<time>` can be written in many ways: 20mins, 1d, 90hours"],
    "unmute": ["Unmute a member in the server.\n\n**Usage**\n```$unmute <user>```\n\n**Example**\n```$unmute @Timmy```", "**Remember:** `<user>` can be a mention or a user ID."],
    "addrole": ["Add a role to a member.\n\n**Usage**\n```$addrole <user> <role>```\n\n**Example**\n```$addrole @Jenny @Moderator```", "**Remember:** `<user>` and `<role>` can be a mention or a <user>/ role ID."],
    "removerole": ["Remove a role from a member.\n\n**Usage**\n```$removerole <user> <role>```\n\n**Example**\n```$removerole @Jenny @Moderator```", "**Remember:** `<user>` and `<role>` can be a mention or a <user>role ID."],
    "messagecount": ["Get the message count of a member's messages from past messages. (100 or less)\n\n**Usage**\n```$messagecount <user> <amount (optional)>```\n\n**Example**\n```$messagecount @Frog 60```", "**Remember:** `<user>` can be a mention or a user ID."],
    # "slowmode": ["Set the slowmode of a channel.\n\n**Usage**\n```$slowmode <time>```\n\n**Example**\n```$slowmode 5```", "**Remember:** `<time>` is in seconds."],
    "softban": ["Softban a member from the server.\n\n**Usage**\n```$softban <user> <reason (optional)>```\n\n**Example**\n```$softban @Matthew Sending IP grabbing links.```", "**Remember:** `<user>` can be a mention or a user ID."],
    "tempban": ["Temporarily ban a member from the server.\n\n**Usage**\n```$tempban <user> <time> <reason (optional)>```\n\n**Example**\n```$tempban @Apple 1d NSFW profile picture.```", "**Remember:** `<user>` can be a mention or a user ID. `<time>` can be written in many ways: `20mins`, `1d`, `90hours`"],
    "settings": ["View or change the bot's settings.\n\n**Usage**\n```$settings [option] [variable] [value]```\n\n**Example**\n```$settings filter guilded_invite_checker enable```", "**Remember:** `[option]` can be `change`. `[variable]` can be `guilded_invite_checker`, `caps_checker`, `link_checker`, `spam_checker`, `emoji_spam_checker`, `mass_mention_checker`. `[value]` can be `enable`, `disable`."]
}