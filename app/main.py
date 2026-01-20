from fastapi import FastAPI, Response, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException

from pydantic import BaseModel
from contextlib import asynccontextmanager

from app.services.url_service import create_hashed_url
from app.core.database import get_db_connect, init_db
from app.repo.url_repository import saveIntoDb, lookIntoDb

import validators

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db() 
    yield

app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

class shortenRequest(BaseModel):
    url_input: str

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
            if saved.status_code == 200:
                response.status_code = status.HTTP_200_OK

            return saved.found_hash

        return hash

@app.get("/shorten/{url_id}")
async def read_url(url_id: str, response: Response, db = Depends(get_db_connect)):

    link = await lookIntoDb(url_id, db)

    if link:
        return RedirectResponse(url=link, status_code=307)
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise StarletteHTTPException(status_code=404)    
    
@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request, exc):
    print(exc)
    if exc.status_code == 404:
        return RedirectResponse(url='http://localhost:5173/404.html', status_code=307)