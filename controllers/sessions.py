from typing import Optional

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, Response
from mako.lookup import TemplateLookup

from models.user import User
from sqlalchemy.orm import Session
from config.database import get_db

sessions_router = APIRouter()
views = TemplateLookup(directories=['views', 'views/session'])

@sessions_router.get("/signin")
def sessions_new(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user-id")
    user = db.query(User).filter_by(id=user_id).first()

    template = views.get_template("/new.html")
    html = template.render(user=user)
    return HTMLResponse(html)

@sessions_router.post("/session")
async def sessions_create(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    email=form["email"]
    password=form["password"]

    user = db.query(User).filter_by(email=email).first()

    # TODO: Validate password

    response = Response(status_code=303)
    response.set_cookie("user-id", user.id)
    response.headers["location"] = "/"
    return response

@sessions_router.delete("/signout")
async def sessions_delete(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user-id")
    user = db.query(User).filter_by(id=user_id).first()

    response = Response(status_code=303)
    response.set_cookie("user-id", None)
    response.headers["location"] = "/"
    return response
