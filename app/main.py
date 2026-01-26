from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

from app.services.url_service import create_hashed_url
from app.core.database import init_db
from app.repo.url_repository import saveIntoDb, lookIntoDb

import validators

init_db()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

class shortenRequest(BaseModel):
    url_input: str
    size_input: int

@app.post("/api/shorten", status_code=201)

def read_root(item: shortenRequest, response: Response):
    user_url = item.url_input
    size_url = item.size_input

    if not user_url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")

    validateUrl = validators.url(user_url)
    if validateUrl != True:
        raise HTTPException(status_code=400, detail="Invalid URL format")

    hash = create_hashed_url(user_url, size_url)
    saved = saveIntoDb(user_url, hash)

    if saved:
        if saved.status_code == 200:
            response.status_code = status.HTTP_200_OK

        return { "hash": hash, "status_code": 200}

    return { "hash": hash, "status_code": 201}

@app.get("/api/shorten/{url_id}")
def read_url(url_id: str, response: Response):

    link = lookIntoDb(url_id)

    if link:
        return RedirectResponse(url=link, status_code=307)
    else:
        raise HTTPException(status_code=404, detail="Invalid Link", )
 
    
@app.exception_handler(StarletteHTTPException)
def custom_404_handler(request, exc):

    match exc.status_code:
        case 404:
            if(request.url.path.startswith('/api/shorten')):
                return JSONResponse(status_code=exc.status_code, content={"detail": "Link not found."})
    
            return RedirectResponse(url='/static/index.html', status_code=307)
    
    return JSONResponse(status_code=exc.status_code, content={"detail": str(exc.detail)})