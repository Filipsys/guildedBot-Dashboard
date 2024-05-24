import guilded
from guilded.ext import tasks, commands
from data.misc.helpcommandtext import *
from data.database.sqlite import *


class HelpCog(commands.Cog):
  """The help cog."""

  def __init__(self, client):
    self.client = client
  
  @commands.command(aliases = ["commands"])
  async def help(self, ctx, command = None):
    prefix = "$"

    try:
      prefix = cursor.execute("SELECT prefix FROM guilds WHERE guild_id = ?", (ctx.guild.id,)).fetchone()[0]
    except:
      pass

    if command is None:
    #   await ctx.send(embed = main_help_embed.description.replace("{prefix}", str(prefix)))
      await ctx.send(embed = main_help_embed)
    else:
      try:
        command_description = commands_text_dict[command][0]
        command_next_field = commands_text_dict[command][1]

      except KeyError:
        return await ctx.send("That command does not exist.")

      embed = guilded.Embed(
        title = f"Help for the {command} command",
        description = f"{command_description}",
        color = guilded.Color.green()
      )
      embed.add_field(
        name = " ",
        value = f"{command_next_field}",
        inline = False
      )

      await ctx.send(embed = embed)


def setup(client):
  client.add_cog(HelpCog(client))