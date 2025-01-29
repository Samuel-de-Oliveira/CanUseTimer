# This file creates the times database
import sqlite3

# TODO: Create a system that works...
# Create DB
times_data_base = sqlite3.connect('timesSaved.db')
times_cursor    = times_data_base.cursor()

database_modality: dict = {
  '3x3': 'Cube3x3',
  '2x2': 'Cube2x2',
  '4x4': 'Cube4x4',
  '5x5': 'Cube5x5',
  '6x6': 'Cube6x6',
  '7x7': 'Cube7x7',
  'pyra': 'Pyra',
  'skewb': 'Skewb',
  'sq1': 'SQ1'
}

def createDataBase() -> None:
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


def loadDataBase() -> dict:
  try:
    resp = times_cursor.execute(f"""
      SELECT time FROM {database_modality["2x2"]}
    """)
    values:     list = resp.fetchall()
    get_values: list = []
    for v in values: 
      print(v[0])
      get_values.append(v[0])

    return {
      '2x2': get_values
    }

  except Exception as exce:
    print(f'Error: {exce}')
    exit()


def saveDataBases() -> None:
  times_data_base.commit()


if __name__ == "__main__": print("Run the Main.py file to start the program...")
