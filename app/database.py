import mysql.connector
import os

db_config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

def init_db():

    connection = mysql.connector.connect(**db_config)

    mycursor = connection.cursor()

    mycursor.execute("CREATE DATABASE IF NOT EXISTS urls")
    mycursor.execute("USE urls")
    mycursor.execute("CREATE TABLE IF NOT EXISTS users_urls (" \
    "url_id int NOT NULL AUTO_INCREMENT UNIQUE," \
    "original_url nvarchar(400) NOT NULL UNIQUE," \
    "newurl varchar(15) NOT NULL PRIMARY KEY" \
    ")")

    connection.commit()
    connection.close()
    print("Database initialized!")

    return

def get_db_connect():

    config_with_db = db_config.copy()
    config_with_db["database"] = "urls" 
    
    connection = mysql.connector.connect(**config_with_db)
    
    try:
        yield connection
    finally:
        connection.close()