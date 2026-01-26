import mysql.connector
import os
import time

from dotenv import load_dotenv
load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"), 
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

app_db_config = {
    **db_config,
    "database": "urls"
}

# Start DB

def init_db():

    connection = False

    retries = 5

    # Sometimes, Docker is initializing the DB.
    # This will make 5 connection attempts 5 seconds apart each.

    while retries > 0:
        try:
            connection = mysql.connector.connect(**db_config)
            break 
        except mysql.connector.Error as err:
            print(f"Database not ready yet... ({err})")
            retries -= 1
            time.sleep(5)
    
    if retries == 0:
        raise Exception("Could not connect to database after 5 attempts.")

    if(connection):

        mycursor = connection.cursor()
        
        # This line is commented because you can only use it with the root user. So if you really want, just change in the db_config.
        # mycursor.execute("CREATE DATABASE IF NOT EXISTS urls")

        mycursor.execute("USE urls")
        mycursor.execute("CREATE TABLE IF NOT EXISTS users_urls (" \
    "url_id int NOT NULL AUTO_INCREMENT UNIQUE," \
    "original_url nvarchar(400) NOT NULL UNIQUE," \
    "newurl varchar(16) NOT NULL PRIMARY KEY" \
    ")")

        connection.commit()
        connection.close()
        print("Database initialized!")

    return

# Get connection

def get_db_connect():
    return mysql.connector.connect(**app_db_config)

# Unifying queries

def execute_query(query, params=None, fetchone=False, fetchall=False):

    connection = get_db_connect()
    cursor = connection.cursor(dictionary=True, buffered=True)

    try:
        cursor.execute(query, params or ())

        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()
        else:
            result = None

        connection.commit()
        return result

    finally:
        cursor.close()
        connection.close()