import sqlite3

from config import DATABASE_PATH


def get_connection():

    return sqlite3.connect(
        DATABASE_PATH
    )


def create_database():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS
        traffic_records (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            vehicle_count INTEGER,

            cars INTEGER,

            motorcycles INTEGER,

            buses INTEGER,

            trucks INTEGER,

            average_speed REAL,

            congestion TEXT,

            green_time INTEGER
        )
    """)


    connection.commit()

    connection.close()


def save_record(
    vehicle_count,
    vehicle_types,
    average_speed,
    congestion,
    green_time
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""
        INSERT INTO traffic_records
        (
            vehicle_count,
            cars,
            motorcycles,
            buses,
            trucks,
            average_speed,
            congestion,
            green_time
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        vehicle_count,

        vehicle_types["car"],

        vehicle_types["motorcycle"],

        vehicle_types["bus"],

        vehicle_types["truck"],

        average_speed,

        congestion,

        green_time
    ))


    connection.commit()

    connection.close()


def get_recent_records(limit=20):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""
        SELECT *
        FROM traffic_records
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))


    records = cursor.fetchall()

    connection.close()


    return records