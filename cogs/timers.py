import guilded
import time as time_module

from guilded.ext import tasks, commands
from data.database.sqlite import *
from data.misc.variables import *


class TimersCog(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.mutecheck.start()
    self.tempbancheck.start()
    self.temprolecheck.start()
    self.code_timeout.start()

  @tasks.loop(seconds = 10)
  async def mutecheck(self):
    """The mute check loop."""

    mutes = cursor.execute("SELECT * FROM mutes").fetchall()

    for mute in mutes:
      if mute[3] < int(time_module.time()):
        guild = await self.client.fetch_server(str(mute[1]))
        member = await guild.fetch_member(str(mute[0]))

        if member and guild:
          mute_role = await guild.fetch_role(MUTED_ROLE_ID)

          if mute_role:
            await member.remove_role(mute_role)

            cursor.execute("DELETE FROM mutes WHERE user_id = ? AND guild_id = ?", (mute[0], mute[1]))
            database.commit()


  @tasks.loop(seconds = 10)
  async def temprolecheck(self):
    """The temprole check loop."""

    temproles = cursor.execute("SELECT * FROM temproles").fetchall()

    for temprole in temproles:
      if temprole[3] < int(time_module.time()):
        guild = await self.client.fetch_server(str(temprole[1]))
        member = await guild.fetch_member(str(temprole[0]))

        if member and guild:
          role = await guild.fetch_role(temprole[2])

          if role:
            await member.remove_role(role)

            cursor.execute("DELETE FROM temproles WHERE user_id = ? AND guild_id = ?", (temprole[0], temprole[1]))
            database.commit()


  @tasks.loop(minutes = 10)
  async def tempbancheck(self):
    """The tempban check loop."""

    bans = cursor.execute("SELECT * FROM tempbans").fetchall()

    for ban in bans:
      if ban[3] < int(time_module.time()):
        guild = await self.client.fetch_server(str(ban[1]))
        member = await guild.fetch_member(str(ban[0]))

        if member and guild:
          await member.unban()

          cursor.execute("DELETE FROM mutes WHERE user_id = ? AND guild_id = ?", (ban[0], ban[1]))
          database.commit()

  @tasks.loop(seconds = 10)
  async def code_timeout(self):
    """The code timeout loop."""

    check_codes = cursor.execute("SELECT code, timestamp_epoch, expired FROM connect_codes").fetchall()

    for check_code in check_codes:
      if int(check_code[2]) == 0:
        if int(check_code[1]) + (10 * 60) < int(time_module.time()):
          cursor.execute("DELETE FROM connect_codes WHERE code = ?", (check_code[0],))
          database.commit()
      else:
        if int(check_code[1]) + (30 * 60) < int(time_module.time()):
          cursor.execute("DELETE FROM connect_codes WHERE code = ?", (check_code[0],))
          database.commit()


def setup(client):
  client.add_cog(TimersCog(client))