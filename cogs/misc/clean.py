import guilded

from guilded.ext import tasks, commands


class CleanCog(commands.Cog):
  """The clean cog."""

  def __init__(self, client):
    self.client = client
  
  @commands.command(aliases = ["cleanup"])
  async def clean(ctx, limit = 10):
    """Cleans up the bot's messages."""

    

def setup(client):
  client.add_cog(CleanCog(client))