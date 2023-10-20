"""Data Loading

This script loads the processed data into the database.

The script takes in a pickle file and outputs a SQLite table.
"""

import pickle
import sqlite3
from time import sleep

DB_PATH = "./data/load_output.db"

def create_db():
    """Creates a local SQLite table

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS areas")

    cursor.execute("""CREATE TABLE areas (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    vertical INTEGER,
                    base INTEGER,
                    summit INTEGER,
                    snowfall INTEGER,
                    trails INTEGER,
                    acres INTEGER,
                    snowmaking INTEGER,
                    longest_run REAL,
                    state TEXT,
                    latitude REAL,
                    longitude REAL
                    );""")

    connection.commit()
    connection.close()

def insert_data(data):
    """Inserts the data row by row into a local SQLite database

    Parameters
    ----------
    data : list
        A list of tuples containing the mountain name and mountain statistics

    Returns
    -------
    None
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.executemany("""INSERT INTO areas (name, vertical, base, summit, snowfall, trails,
                    acres, snowmaking, longest_run, state, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", data)
    connection.commit()
    connection.close()

def main():
    print("Running the load script")
    cleaned_data = pickle.load(open('./data/transform_output.pkl', 'rb'))
    create_db()
    insert_data(cleaned_data)
    print("The processed data has been loaded into the database")

if __name__ == "__main__":
    main()
