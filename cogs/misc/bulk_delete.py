import guilded

from guilded.ext import commands


class BulkMuteCog(commands.Cog):
  """The 'bulk mute' cog."""

  def __init__(self, client):
    self.client = client

  @commands.command(aliases = ["bulk_remove", "bulkremove", "bulkdelete", "bulk_remove", "bulkremove", "bulkdelete"])
  # @commands.has_permissions(manage_messages = True)
  async def bulk_delete(self, ctx, amount = 5):
    """Bulk delete the bot's messages."""

    await ctx.channel.purge(limit = amount, bulk = False)

async def setup(client):
  await client.add_cog(BulkMuteCog(client))