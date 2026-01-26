import mysql.connector
from dataclasses import dataclass
from app.core.database import execute_query
from typing import cast, Dict, Any

@dataclass
class SaveResult:
    found_hash: str | None
    status_code: int=200

def saveIntoDb(original: str, hashed: str):
    
    try:
        result = execute_query(
            "INSERT INTO users_urls (original_url, newurl) VALUES (%s, %s)",
            (original, hashed)
        )
        return SaveResult(found_hash=hashed, status_code=201)
    except mysql.connector.Error as e:

        # err 1062 = already exists in db
        # else, some other error... 

        if(e.errno == 1062):
            res = lookForExisting(hashed)
            if res:
                return SaveResult(found_hash=hashed, status_code=200)
        else:
            print(f"Error saving to DB: {e}")
            return SaveResult(found_hash=None, status_code=999)

# Function to search into DB for the original_url after the GET

def lookIntoDb(url: str):

    result = execute_query(
        "SELECT original_url FROM users_urls WHERE newurl = %s",
        (url,),
        fetchone=True
    )

    if result:
        # Casting the result_dict cuz Pylance was complaining about the dict.
        result_dict = cast(Dict[str, Any], result)
        return result_dict['original_url']

    return None

def lookForExisting(url: str):

    result = execute_query(
        "SELECT original_url FROM users_urls WHERE newurl = %s",
        (url,)
    )

    if result:
        print(result)
        return result
    return None