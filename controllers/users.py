from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response
from mako.lookup import TemplateLookup

from models.user import User
from config.database import Session

users_router = APIRouter()
views = TemplateLookup(directories=['views', 'views/user'])

@users_router.get("/signup")
def users_new():
    user = User()
    template = views.get_template("/new.html")
    html = template.render(user=user)
    return HTMLResponse(html)

@users_router.post("/profile")
async def users_create(request: Request):
    form = await request.form()
    user = User(
            email=form["email"],
            password=form["password"]
            )
    session = Session()
    session.add(user)
    session.commit()

    response = Response(status_code=303)
    response.headers["location"] = "/"
    return response

@users_router.get("/profile")
def users_read(id:int):
    session = Session()
    user = session.query(User).filter_by(id=id).first()

    template = views.get_template("/show.html")
    html = template.render(user=user)
    return HTMLResponse(html)

@users_router.get("/profile/edit")
def users_edit(id:int):
    session = Session()
    user = session.query(User).filter_by(id=id).first()

    template = views.get_template("/edit.html")
    html = template.render(user=user)
    return HTMLResponse(html)

@users_router.put("/profile")
async def users_update(id: int, request: Request):
    form = await request.form()
    session = Session()
    user = session.query(User).filter_by(id=id).first()
    user.email = form["email"]
    user.password = form["password"]
    session.add(user)
    session.commit()

    response = Response(status_code=303)
    response.headers["location"] = "/"
    return response

@users_router.delete("/profile")
def users_delete(id: int):
    session = Session()
    user = session.query(User).filter_by(id=id).first()
    session.delete(user)
    session.commit()

    response = Response(status_code=303)
    response.headers["location"] = "/"
    return response

