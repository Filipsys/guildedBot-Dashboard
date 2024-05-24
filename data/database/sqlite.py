import sqlite3

database = sqlite3.connect("data/database/database.db")
cursor = database.cursor()