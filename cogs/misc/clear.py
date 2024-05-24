import guilded

from guilded.ext import commands


class ClearCog(commands.Cog):
  """The 'clear' cog."""

  def __init__(self, client):
    self.client = client
  
  @commands.command(aliases = ["clear", "delete", "del"])
  # @commands.has_permissions(manage_messages = True)
  async def purge(ctx, amount = 5):
    """Clear messages in the channel."""

    await ctx.channel.purge(limit = amount)

async def setup(client):
  await client.add_cog(ClearCog(client))