from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response
from mako.lookup import TemplateLookup

from models.user import User
from config.database import Session

sessions_router = APIRouter()
views = TemplateLookup(directories=['views', 'views/session'])

@sessions_router.get("/signin")
def sessions_new():
    template = views.get_template("/new.html")
    html = template.render()
    return HTMLResponse(html)

@sessions_router.post("/session")
async def sessions_create(request: Request):
    form = await request.form()
    email=form["email"],
    password=form["password"]

    session = Session()
    #TODO Search for User
    # Validate password
    # Create a session

    response = Response(status_code=303)
    response.headers["location"] = "/"
    return response

@sessions_router.delete("/signout")
async def sessions_delete(request: Request):

    #TODO Search for User
    # Remove from Session

    response = Response(status_code=303)
    response.headers["location"] = "/"
    return response
