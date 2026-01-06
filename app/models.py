import mysql.connector
from dataclasses import dataclass

@dataclass
class SaveResult:
    found_link: str

async def saveIntoDb(original: str, hashed: str, conn):

    cursor = conn.cursor()
    sql = "INSERT INTO users_urls (original_url, newurl) VALUES (%s, %s)"
    
    try:
        cursor.execute(sql, (original, hashed))
        conn.commit()
    except mysql.connector.Error as e:

        if(e.errno == 1062):
            res = await lookForExisting(hashed, conn)
            if res:
                return SaveResult(found_link=res)
        else:
            print(f"Error saving to DB: {e}")
            conn.rollback()
    finally:    
        cursor.close()

async def lookIntoDb(url: str, conn):

    cursor = conn.cursor()
    sql = "SELECT original_url FROM users_urls WHERE newurl = %s"

    q = cursor.execute(sql, (url,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        return result[0]
    return None

async def lookForExisting(url: str, conn):

    cursor = conn.cursor()
    sql = "SELECT newurl FROM users_urls WHERE original_url = %s"

    q = cursor.execute(sql, (url,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        return result[0]
    return None