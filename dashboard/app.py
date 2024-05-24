import sqlite3
import secrets
import time
import sys
import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, session

from datetime import timedelta

app = Flask(__name__, template_folder = "templates")

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes = 30)
app.secret_key = secrets.token_hex(32)


session_timeout = 1800

def get_session_time_left(session_time_start):
  if "user_authenticated" in session:
    current_time = int(datetime.datetime.now().timestamp())

    time_left = (int(session_time_start) + session_timeout) - current_time

    return f"{time_left // 60}:{time_left % 60}"
  else:
    return None


@app.route("/")
@app.route("/startpage")
def startpage():
  return render_template("startpage.html")


@app.route("/dashboard")
def dashboard():
  if "user_authenticated" in session:
    return render_template("dashboard.html")
  else:
    return redirect(url_for("login"))
  

@app.route("/update_guild_variables", methods = ["POST"])
def update_guild_variables():
  if "user_authenticated" in session:
    data = request.json

    database = sqlite3.connect("data/database/database.db")
    cursor = database.cursor()

    # {
    #     "setting": "SETTING", "value": "ENABLED"
    # }

    cursor.execute("SELECT * FROM guild_variables WHERE guild_id = ? AND variable = ?", (session["guild_id"], data["setting"]))
    result = cursor.fetchone()

    if result is not None:
      cursor.execute("UPDATE guild_variables SET value = ? WHERE guild_id = ? AND variable = ?", (data["value"], session["guild_id"], data["setting"]))
      database.commit()
    else:
      cursor.execute("INSERT INTO guild_variables VALUES (?, ?, ?)", (session["guild_id"], data["setting"], data["value"]))
      database.commit()

    database.close()

    return jsonify({"status": "success"})
  else:
    return redirect(jsonify({"status": "error", "message": "User not authenticated"}))

  
@app.route("/get_data", methods = ["POST"])
def get_data():
  if "user_authenticated" in session:
    database = sqlite3.connect("data/database/database.db")
    cursor = database.cursor()

    cursor.execute("SELECT * FROM latest_bot_updates_dashboard ORDER BY update_id DESC LIMIT 5")
    result_1 = cursor.fetchall()

    cursor.execute("SELECT * FROM main_server_data_dashboard")
    result_2 = cursor.fetchall()

    cursor.execute("SELECT * FROM mod_command_history WHERE guild_id = ?", (session["guild_id"],))
    result_3 = cursor.fetchall()

    cursor.execute("SELECT * FROM bot_info_dashboard")
    result_4 = cursor.fetchall()

    cursor.execute("SELECT * FROM guild_variables WHERE guild_id = ?", (session["guild_id"],))
    result_5 = cursor.fetchall()

    print(result_5)

    tmstmp = cursor.execute("SELECT value FROM bot_info_dashboard WHERE variable = 'STARTUP_TIMESTAMP_EPOCH'").fetchone()[0]
    uptime_timestamp = datetime.datetime.now().timestamp() - float(tmstmp)



    uptime_hours = uptime_timestamp // 3600
    uptime_timestamp %= 3600
    uptime_minutes = uptime_timestamp // 60
    uptime_timestamp %= 60
    uptime_seconds = uptime_timestamp

    uptime_timestamp = f"{int(uptime_hours)}h {int(uptime_minutes)}m {int(uptime_seconds)}s"

    data_1, data_2, data_3, data_4, data_5, data_6, data_7 = [], [], [], [], [], [], []


    for row in result_1:
      data_1.append({"update_id": row[0], "update_title": row[1], "update_description": row[2], "update_date": row[3]})

    for row in result_2:
      data_2.append({"guild_id": row[0], "server_name": row[1], "server_description": row[2], "server_members": row[3], "category_count": row[4], "text_channel_count": row[5], "voice_channel_count": row[6], "role_count": row[7], "server_owner": row[8], "server_owner_id": row[9], "server_icon": row[10], "member_count": row[11], "messages_sent": row[12], "messages_sent_timestamp": row[13], "messages_edited": row[14], "messages_edited_timestamp": row[15], "messages_deleted": row[16], "messages_deleted_timestamp": row[17], "mod_cmds_ran": row[18], "mod_cmds_ran_timestamp": row[19]})

    for row in result_3:
      time_str_converted = time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(row[10]))

      data_3.append({"target_id": row[0], "target_name": row[1], "executor_id": row[2], "executor_name": row[3], "executor_profile_picture_url": row[4], "executor_role": row[5], "guild_id": row[6], "guild_name": row[7], "action": row[8], "additional_info": row[9], "timestamp": time_str_converted, "reason": row[11]})

    data_4.append({"bot_version": result_4[0][1], "bot_uptime": str(uptime_timestamp), "guild_count": result_4[1][1]})

    for row in result_5:
      ALL_VARIABLES_LIST = [
        "ADMIN_IMMUNITY",
        "INHERIT_GUILDED_PERMISSIONS",
        "INVITE_CHECKER",
        "CAPS_CHECKER",
        "LINK_CHECKER",
        "SAFE_BROWSING_CHECKER",
        "NSFW_IMAGE_CHECKER",
        "SPAM_CHECKER",
        "EMOJI_SPAM_CHECKER",
        "MASS_MENTION_CHECKER",
        "NEW_ACCOUNT_CHECKER",
        "ADVANCED_CUSTOMISATION",
        "INFRACTION_CUSTOMISATION",
      ]

      ALL_MISC_VARIABLES_LIST = [
        "MUTED_ROLE",
        "SETTINGS_MSG",
        "MISC_MSG",
        "LOGS_CHANNEL",
        "LOGGING_STYLE",
        "ALL_CHANNELS"
      ]


      if row[1] in ALL_VARIABLES_LIST:
        if row[2] == "ENABLED":
          data_5.append(f"{row[1]}: ENABLED")
        else:
          data_5.append(f"{row[1]}: DISABLED")

      else:
        if row[1] not in ["MUTED_ROLE", "SETTINGS_MSG", "MISC_MSG", "LOGS_CHANNEL", "LOGGING_STYLE", "ALL_CHANNELS"]:
          data_5.append(f"{row[1]}: DISABLED")
      
        if row[1] not in ALL_VARIABLES_LIST:
          if row[1] in ALL_MISC_VARIABLES_LIST:
            # data_6.append({row[1]: row[2]})
            data_6.append(f"{row[1]}: {row[2]}")
          else:
            # data_6.append({row[1]: None})
            data_6.append(f"{row[1]}: None")

    missing_variables = set(ALL_VARIABLES_LIST) - set([item.split(":")[0] for item in data_5])
    for variable in missing_variables:
      data_5.append(f"{variable}: DISABLED")

    data_5.sort(key = lambda x: [
      "ADMIN_IMMUNITY",
      "INHERIT_GUILDED_PERMISSIONS",
      "INVITE_CHECKER",
      "CAPS_CHECKER",
      "LINK_CHECKER",
      "SAFE_BROWSING_CHECKER",
      "NSFW_IMAGE_CHECKER",
      "SPAM_CHECKER",
      "EMOJI_SPAM_CHECKER",
      "MASS_MENTION_CHECKER",
      "NEW_ACCOUNT_CHECKER",
      "ADVANCED_CUSTOMISATION",
      "INFRACTION_CUSTOMISATION"
    ].index(x.split(":")[0]))
  
    data_7.append({"session_time_left": get_session_time_left(session["timestamp_epoch"])})


    data_8 = []
    all_channels = cursor.execute("SELECT value FROM guild_variables WHERE guild_id = ? AND variable = 'ALL_CHANNELS'", (session["guild_id"],)).fetchone()[0]

    if all_channels is not None:
      all_channels = all_channels[:-3]
      all_channels = all_channels.split(",,,")

      for channel in all_channels:
        channel_id, channel_name = channel.split(":::")[0], channel.split(":::")[1]

        data_8.append({'channel_id': f'{channel_id}', 'channel_name': f'{channel_name}'})

    database.close()


    return jsonify({"latest_bot_updates_data": data_1, "main_server_data": data_2, "mod_command_history": data_3, "bot_info": data_4, "guild_variables": data_5, "misc_guild_variables": data_6, "timer_data": data_7, "all_channels": str(data_8)})
  else:
    return redirect(jsonify({"status": "error", "message": "User not authenticated"}))


@app.route("/login")
def login():
  if "hash" in request.args:
    received_hash = request.args.get("hash")

    database = sqlite3.connect("data/database/database.db")
    cursor = database.cursor()

    cursor.execute("SELECT * FROM connect_codes WHERE code = ?", (received_hash,))
    result = cursor.fetchone()

    if result is not None:
      cursor.execute("UPDATE connect_codes SET expired = 1 WHERE code = ?", (received_hash,))
      database.commit()

    database.close()

    if result is not None:
      session["user_authenticated"] = True

      session["hash"] = received_hash
      session["guild_id"] = result[0]
      session["timestamp_epoch"] = result[2]
      return redirect(url_for("dashboard"))
    else:
      return redirect(url_for("login"))
    
  return render_template("login.html")


@app.route("/handle_hash", methods = ["POST"])
def handle_hash():
  data = request.json

  received_hash = data.get("hash")

  database = sqlite3.connect("data/database/database.db")
  cursor = database.cursor()

  cursor.execute("SELECT * FROM connect_codes WHERE code = ?", (received_hash,))
  result = cursor.fetchone()
  database.close()


  try:
    if result[2] == 1:
      return jsonify({"status": "error", "expired": 1})
  except TypeError:
    pass

  if result is not None:
    return jsonify({"status": "success", "expired": 0})
  else:
    return jsonify({"status": "error", "expired": 0})


if __name__ == "__main__":
  app.run(debug = True)