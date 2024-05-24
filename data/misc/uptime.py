import datetime
import sys
import sqlite3


# database = sqlite3.connect("data/database/database.db")
# cursor = database.cursor


def reset_uptime():
  """Resets the uptime variable."""
  # cursor.execute("CREATE TABLE IF NOT EXISTS bot_info_dashboard (variable TEXT NOT NULL, value TEXT NOT NULL)")

  # check_empty = cursor.execute("SELECT value FROM bot_info_dashboard WHERE variable = 'STARTUP_TIMESTAMP_EPOCH'").fetchone()

  # if check_empty is None:
  #   cursor.execute("INSERT INTO bot_info_dashboard (variable, value) VALUES ('STARTUP_TIMESTAMP_EPOCH', ?)", (str(datetime.datetime.now().timestamp()),))
  # else:
  #   cursor.execute("UPDATE bot_info_dashboard SET value = ? WHERE variable = 'STARTUP_TIMESTAMP_EPOCH'", (str(datetime.datetime.now().timestamp()),))

  # database.commit()


def get_uptime():
  """Returns the uptime."""

  # varone = cursor.execute("SELECT value FROM bot_info_dashboard WHERE variable = 'STARTUP_TIMESTAMP_EPOCH'").fetchone()[0]

  # return int(varone) - datetime.datetime.now().timestamp()