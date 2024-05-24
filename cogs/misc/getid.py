import guilded

from guilded.ext import tasks, commands


class IdCog(commands.Cog):
  """The clear cog."""

  def __init__(self, client):
    self.client = client
  
  @commands.command(aliases = ["getid"])
  async def id(ctx, object):
    if isinstance(object, guilded.Member):
      await ctx.send(f"ID: {object.id}")
    elif isinstance(object, guilded.Role):
      await ctx.send(f"ID: {object.id}")
    elif isinstance(object, guilded.TextChannel):
      await ctx.send(f"ID: {object.id}")
    elif isinstance(object, guilded.VoiceChannel):
      await ctx.send(f"ID: {object.id}")
    else:
      await ctx.send("Sorry! I couldn't find the ID of the object you specified.")

def setup(client):
  client.add_cog(IdCog(client))