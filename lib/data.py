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

# 4x4Cube
times_cursor.execute("""
  CREATE TABLE IF NOT EXISTS Cube4x4 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time REAL NOT NULL
  );
""")

# 5x5Cube
times_cursor.execute("""
  CREATE TABLE IF NOT EXISTS Cube5x5 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time REAL NOT NULL
  );
""")

# 6x6Cube
times_cursor.execute("""
  CREATE TABLE IF NOT EXISTS Cube6x6 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time REAL NOT NULL
  );
""")

# 7x7Cube
times_cursor.execute("""
  CREATE TABLE IF NOT EXISTS Cube7x7 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time REAL NOT NULL
  );
""")

# Pyranminx
times_cursor.execute("""
  CREATE TABLE IF NOT EXISTS Pyra (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time REAL NOT NULL
  );
""")

# Skewb
times_cursor.execute("""
  CREATE TABLE IF NOT EXISTS Skewb (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time REAL NOT NULL
  );
""")

# Square one
times_cursor.execute("""
  CREATE TABLE IF NOT EXISTS SQ1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time REAL NOT NULL
  );
""")

if __name__ == "__main__": print("Run the Main.py file to start the program...")
