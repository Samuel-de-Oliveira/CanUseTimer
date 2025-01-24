# This file creates the times database
import sqlite3

# TODO: Create a system that works...
# Create DB
times_data_base = sqlite3.connect('timesSaved.db')
times_cursor    = times_data_base.cursor()

# Create table
# 3x3Cube
times_cursor.execute("""
  CREATE TABLE IF NOT EXISTS Cube3x3 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time REAL NOT NULL
  );
""")

# 2x2Cube
times_cursor.execute("""
  CREATE TABLE IF NOT EXISTS Cube2x2 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time REAL NOT NULL
  );
""")

if __name__ == "__main__": print("Run the Main.py file to start the program...")
