import guilded

from guilded.ext import commands
from data.database.sqlite import *


class MessageCountCog(commands.Cog):
  """The message count cog."""

  def __init__(self, client):
    self.client = client

  @commands.command(aliases = ["messagecount", "countmessages"])
  @commands.has_server_permissions(manage_messages = True)
  async def message_count(self, ctx, member, channel, amount = 50):

    check_guild_exists = cursor.execute("SELECT guild_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,)).fetchone()
    if check_guild_exists is None:
      return await ctx.send("Please run the `$start` command first.")
    
    if amount > 100:
      return await ctx.send("You can only count messages up to 100.")

    if str(member)[0] == "@":
      member = await commands.MemberConverter().convert(ctx, str(member).replace("@", ""))
    else:
      member = await commands.MemberConverter().convert(ctx, member)
    
    if str(channel)[0] == "#":
      channel = await commands.TextChannelConverter().convert(ctx, channel.replace("#", ""))
    else:
      channel = await commands.TextChannelConverter().convert(ctx, channel)

    counter = 0

    for message in await channel.history(limit = amount):
      if message.author == member:
        counter += 1

    await ctx.send(f"{member.name} has sent {counter} messages in the last {amount} messages.")


def setup(client):
  client.add_cog(MessageCountCog(client))