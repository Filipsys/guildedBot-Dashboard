import guilded
from guilded.ext import commands


class YouCog(commands.Cog):
  """The 'you' cog."""

  def __init__(self, client):
    self.client = client

  @commands.command()
  async def you(self, ctx, m):
    """The 'you' command."""

    member = await commands.MemberConverter().convert(ctx, str(m).replace("@", ""))

    embed = guilded.Embed(
      title = "You",
      description = f"You are {member.mention}.",
      color = guilded.Color.green()
    )

    await ctx.reply(embed = embed)


def setup(client):
  client.add_cog(YouCog(client))