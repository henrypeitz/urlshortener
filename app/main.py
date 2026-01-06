from typing import Union
from fastapi import FastAPI, Response, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from services import create_hashed_url
from database import get_db_connect, init_db
from models import saveIntoDb, lookIntoDb

import validators

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

class shortenRequest(BaseModel):
    url_input: str

init_db()

@app.post("/shorten", status_code=201)
async def read_root(item: shortenRequest, response: Response, db = Depends(get_db_connect)):
    user_url = item.url_input

    if user_url == '':
        response.status_code = status.HTTP_400_BAD_REQUEST


    validateUrl = validators.url(user_url)
    if validateUrl != True:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return
    else:
        hash = create_hashed_url(user_url)
        saved = await saveIntoDb(user_url, hash, db)

        if saved:
            return saved.found_link

        return hash

@app.get("/shorten/{url_id}")
async def read_url(url_id: str, response: Response, db = Depends(get_db_connect)):

    link = await lookIntoDb(url_id, db)

    if link:
        return RedirectResponse(url=link, status_code=307)
    else:
        return {"Error": 404}