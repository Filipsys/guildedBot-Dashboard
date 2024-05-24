import guilded
import urllib.parse
import requests
import re
import os

from nudenet import NudeDetector
from dotenv import load_dotenv
from guilded.ext import commands

from data.database.sqlite import *
from data.misc.setting_embed_function import create_logging_embed


load_dotenv(dotenv_path = "BOTS\default\secrets.env")

nude_detector = NudeDetector()


def check_admin_immunity(message):
  """Check if a user has admin immunity."""

  check_admin_setting = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("ADMIN_IMMUNITY", message.guild.id)).fetchone()[0]

  if check_admin_setting == "ENABLED":
    if message.author.guild_permissions.administrator:
      return True
    else:
      return False
  
  return False


async def check_guilded_invite(message):
  """Check if a message contains a Guilded invite."""

  if message.author.bot:
    return
  
  if check_admin_immunity(message):
    return
  

  if ("guilded.gg" in message.content or "guilded.com" in message.content) and not "amazonaws.com" in message.content:
    await message.delete()

    logs_channel_id = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("LOGS_CHANNEL", message.guild.id)).fetchone()[0]

    if logs_channel_id:
      channel = await message.guild.getch_channel(logs_channel_id)

      embed = guilded.Embed(description = f":discord-eq: **{message.author} sent a Guilded invite link in {message.channel}.**\n```{message.content}```")
      embed.set_footer(text = f"User ID: {message.author.id}  ||  Channel ID: {message.channel.id}")

      await channel.send(embed = embed)
    
    member = await message.guild.getch_member(message.author.id)
    await message.channel.send(f"{member.display_name}, please don't send Guilded invite links in this channel.", delete_after = 10)


async def check_caps(message):
  """Check if a message contains too many capital letters."""

  if message.author.bot:
    return
  
  if check_admin_immunity(message):
    return

  await message.channel.send("checking for caps")

  uppercase_count = 0

  for letter in message.content:
    if letter in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]:
      uppercase_count += 1
    
  if len(message.content) - uppercase_count < len(message.content) / 3:
    logs_channel_id = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("LOGS_CHANNEL", message.guild.id)).fetchone()[0]

    if logs_channel_id:
      channel = await message.guild.getch_channel(logs_channel_id)

      # embed = guilded.Embed(description = f":discord-eq: **{message.author.display_name} sent a message with too many capital letters in {message.channel}.**\n```{message.content}```")
      # embed.set_footer(text = f"User ID: {message.author.id}  ||  Channel ID: {message.channel.id}")

      await channel.send(embed = create_logging_embed(msg = message, action = "sent a message with too many capital letters", message = message.content))

    await message.delete()

    member = await message.guild.getch_member(message.author.id)
    await message.channel.send(f"{member.display_name}, please don't spam in this channel.", delete_after = 10)
  

async def check_links(message):
  """Check if a message contains a link."""

  if message.author.bot:
    return
  
  if check_admin_immunity(message):
    return
  
  if re.search(r"(http://|https://|www\.)", message.content):
    await message.delete()

    logs_channel_id = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("LOGS_CHANNEL", message.guild.id)).fetchone()[0]

    if logs_channel_id:
      channel = await message.guild.getch_channel(logs_channel_id)

      embed = guilded.Embed(description = f":discord-eq: **{message.author.display_name} sent a link in {message.channel}.**\n```{message.content}```")
      embed.set_footer(text = f"User ID: {message.author.id}  ||  Channel ID: {message.channel.id}")

      await channel.send(embed = embed)

    member = await message.guild.getch_member(message.author.id)
    await message.channel.send(f"{member.display_name}, please don't send links in this channel.", delete_after = 10)


async def check_unsafe_links(message):
  """Check if a message contains an unsafe link."""

  if message.author.bot:
    return
  
  if check_admin_immunity(message):
    return

  if re.search(r"(http://|https://|www\.)", message.content):
    match = re.search(r"(http://|https://|www\.)\S+", message.content)

    if match:
      url = match.group(0)

    if "#" in url:
      url = url.split("#", 1)[0]

    while "%" in url:
      url = urllib.parse.unquote(url)

    if not urllib.parse.urlparse(url).path:
      url += "/"


    async def authenticate_with_api_key(api_key: str, link: str) -> None:
      threat_info = {
        "threatInfo": {
          "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "THREAT_TYPE_UNSPECIFIED", "POTENTIALLY_HARMFUL_APPLICATION", "UNWANTED_SOFTWARE"],
          "platformTypes": ["ANY_PLATFORM"],
          "threatEntryTypes": ["URL"],
          "threatEntries": [{"url": link}]
        }
      }

      response = requests.post(
        f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}",
        headers = {"Content-Type": "application/json"},
        json = threat_info
      )

      if response.status_code == 200:
        threat_matches = response.json().get("matches", [])

        if threat_matches:
          print("The URL is a potential threat. Details:")

          for match in threat_matches:
            print(f"- Threat type: {match['threatType']}, platform type: {match['platformType']}")

          await message.delete()

          logs_channel_id = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("LOGS_CHANNEL", message.guild.id)).fetchone()[0]

          if logs_channel_id:
            channel = await message.guild.getch_channel(logs_channel_id)

            embed = guilded.Embed(description = f":discord-eq: **{message.author.display_name} sent an unsafe / harmful link in {message.channel}.**\n```{message.content}```")
            embed.set_footer(text = f"User ID: {message.author.id}  ||  Channel ID: {message.channel.id}")

            await channel.send(embed = embed)

          member = await message.guild.getch_member(message.author.id)
          await message.channel.send(f"{member.display_name}, please don't send harmful links in this channel.", delete_after = 10)
        else:
          pass  
      else:
        print("Error:", response.status_code, response.text)


    await authenticate_with_api_key(os.getenv('GOOGLE_API_TOKEN'), url)


async def check_nsfw_image(message):
  """Check if a message contains an NSFW image."""

  if message.author.bot:
    return
  
  if check_admin_immunity(message):
    return

  # all_labels = [
  #   "FEMALE_GENITALIA_COVERED",
  #   "FACE_FEMALE",
  #   "BUTTOCKS_EXPOSED",
  #   "FEMALE_BREAST_EXPOSED",
  #   "FEMALE_GENITALIA_EXPOSED",
  #   "MALE_BREAST_EXPOSED",
  #   "ANUS_EXPOSED",
  #   "FEET_EXPOSED",
  #   "BELLY_COVERED",
  #   "FEET_COVERED",
  #   "ARMPITS_COVERED",
  #   "ARMPITS_EXPOSED",
  #   "FACE_MALE",
  #   "BELLY_EXPOSED",
  #   "MALE_GENITALIA_EXPOSED",
  #   "ANUS_COVERED",
  #   "FEMALE_BREAST_COVERED",
  #   "BUTTOCKS_COVERED",
  # ]

  high_risk_labels = [
    "BUTTOCKS_EXPOSED",
    "FEMALE_BREAST_EXPOSED",
    "FEMALE_GENITALIA_EXPOSED",
    "MALE_GENITALIA_EXPOSED",
    "ANUS_EXPOSED",
  ]

  mid_risk_labels = [
    "MALE_BREAST_EXPOSED",
    "FEMALE_BREAST_COVERED",
    "BUTTOCKS_COVERED",
    "ANUS_COVERED",
    "BELLY_EXPOSED",
    "FEET_EXPOSED",
  ]

  low_risk_labels = [
    "BELLY_COVERED",
    "FEET_COVERED",
    "ARMPITS_COVERED",
    "ARMPITS_EXPOSED",
    "FACE_MALE",
    "FACE_FEMALE",
  ]

  if message.attachments:
    for attachment in message.attachments:
      if attachment.filename.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
        result = nude_detector.detect("image.png")

        if result:
          high_risk = [label for label in high_risk_labels if label in result]
          mid_risk = [label for label in mid_risk_labels if label in result]
          low_risk = [label for label in low_risk_labels if label in result]

          risk_rating = None

          if mid_risk:
            risk_rating = "HIGH"
          elif high_risk:
            risk_rating = "MEDIUM"
          elif low_risk:
            risk_rating = "LOW"


          if risk_rating == "HIGH" or risk_rating == "MEDIUM":
            await message.delete()

            logs_channel_id = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("LOGS_CHANNEL", message.guild.id)).fetchone()[0]

            if logs_channel_id:
              channel = await message.guild.getch_channel(logs_channel_id)


              result_string = ""
              for class_r in result:
                result_string += f"{class_r['class']} - score: {class_r['score']}\n"

              embed = guilded.Embed(description = f":discord-eq: **{message.author.display_name} sent an NSFW image in {message.channel} with a risk rating of {risk_rating}.**\n\nImage contained the following:```{result_string}```")
              embed.set_footer(text = f"User ID: {message.author.id}  ||  Channel ID: {message.channel.id}")

              await channel.send(embed = embed)

            member = await message.guild.getch_member(message.author.id)
            await message.channel.send(f"{member.display_name}, please don't send NSFW images in this channel.", delete_after = 10)
          # else:
          #   await message.add_reaction("90001164")




user_queues = {}
async def check_spam(message):
    """Check if a message is spam."""

    if message.author.bot:
      return
    
    if check_admin_immunity(message):
      return

    if message.author.id not in user_queues:
      user_queues[message.author.id] = []
        
    user_queues[message.author.id].append({letter: message.content.count(letter) for letter in set(message.content) if letter.isalpha()})
    
    if len(user_queues[message.author.id]) > 5:
      user_queues[message.author.id].pop(0)
    
    if len(user_queues[message.author.id]) < 5:
      return
    
    total_letter_count = sum(sum(word_dict.values()) for word_dict in user_queues[message.author.id])
    letter_counts = [word_dict for word_dict in user_queues[message.author.id]]
    
    if all(letter_counts[0] == letter_count for letter_count in letter_counts[1:]):
      if sum(letter_counts[0].values()) >= 0.9 * total_letter_count:
        await message.delete()

        logs_channel_id = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("LOGS_CHANNEL", message.guild.id)).fetchone()[0]

        if logs_channel_id:
          channel = await message.guild.getch_channel(logs_channel_id)

          embed = guilded.Embed(description = f":discord-eq: **{message.author.display_name} sent a spam message in {message.channel}.**\n```{message.content}```")
          embed.set_footer(text = f"User ID: {message.author.id}  ||  Channel ID: {message.channel.id}")

          await channel.send(embed = embed)

        member = await message.guild.getch_member(message.author.id)
        return await message.channel.send(f"{member.display_name}, please don't spam in this channel.", delete_after = 10)



async def check_emoji_spam(message):
  """Check if a message contains too many emojis."""

  if message.author.bot:
    return
  
  if check_admin_immunity(message):
    return

  message.content = message.content.replace("::", ": :")
  emoji_count = 0

  for word in message.content.split():
    if word.startswith(":") and word.endswith(":"):
      emoji_count += 1

  if emoji_count > 8:
    await message.delete()

    logs_channel_id = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("LOGS_CHANNEL", message.guild.id)).fetchone()[0]

    if logs_channel_id:
      channel = await message.guild.getch_channel(logs_channel_id)

      embed = guilded.Embed(description = f":discord-eq: **{message.author.display_name} sent a message with too many emojis in {message.channel}.**\n```{message.content}```")
      embed.set_footer(text = f"User ID: {message.author.id}  ||  Channel ID: {message.channel.id}")

      await channel.send(embed = embed)

    member = await message.guild.getch_member(message.author.id)
    await message.channel.send(f"{member.display_name}, please don't spam in this channel.", delete_after = 10)


async def check_mass_mentions(message):
  """Check if a message contains too many mentions."""

  if message.author.bot:
    return
  
  if check_admin_immunity(message):
    return

  if len(message.mentions) > 4 or len(message.raw_role_mentions) > 4:
    await message.delete()

    logs_channel_id = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("LOGS_CHANNEL", message.guild.id)).fetchone()[0]

    if logs_channel_id:
      channel = await message.guild.getch_channel(logs_channel_id)

      embed = guilded.Embed(description = f":discord-eq: **{message.author.display_name} sent a message with too many mentions in {message.channel}.**\n```{message.content}```")
      embed.set_footer(text = f"User ID: {message.author.id}  ||  Channel ID: {message.channel.id}")

      await channel.send(embed = embed)

    member = await message.guild.getch_member(message.author.id)
    await message.channel.send(f"{member.display_name}, please don't spam mentions in this channel.", delete_after = 10)


async def check_new_account(message):
  """Check if a user is a new account."""

  if message.author.bot:
    return
  
  if check_admin_immunity(message):
    return
  
  new_account_threshold = 60 * 60 * 24 * 7

  print(message.author.created_at)
  print(message.created_at)

  if message.author.created_at > message.created_at - new_account_threshold:
    await message.delete()

    logs_channel_id = cursor.execute("SELECT value FROM guild_variables WHERE variable = ? AND guild_id = ?", ("LOGS_CHANNEL", message.guild.id)).fetchone()[0]

    if logs_channel_id:
      channel = await message.guild.getch_channel(logs_channel_id)

      embed = guilded.Embed(description = f":discord-eq: **{message.author.display_name} sent a message with a new account in {message.channel}.**\n```{message.content}```")
      embed.set_footer(text = f"User ID: {message.author.id}  ||  Channel ID: {message.channel.id}")

      await channel.send(embed = embed)

    member = await message.guild.getch_member(message.author.id)
    await message.channel.send(f"{member.display_name}, please don't use new accounts in this channel.", delete_after = 10)