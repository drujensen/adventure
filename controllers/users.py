from typing import Optional

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, Response
from mako.lookup import TemplateLookup

from models.user import User
from sqlalchemy.orm import Session
from config.database import get_db
import bcrypt

users_router = APIRouter()
views = TemplateLookup(directories=['views', 'views/user'])

@users_router.get("/signup")
def users_new(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user-id")
    user = db.query(User).filter_by(id=user_id).first()

    template = views.get_template("/new.html")
    html = template.render(user=user)
    return HTMLResponse(html)

@users_router.post("/profile")
async def users_create(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    email = form["email"]
    hashed_password = bcrypt.hashpw(form["password"].encode("utf-8"), bcrypt.gensalt())
    user = User(
        email=email,
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    response = Response(status_code=303)
    response.set_cookie("user-id", user.id)
    response.headers["location"] = "/"
    return response

@users_router.get("/profile")
def users_read(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user-id")
    user = db.query(User).filter_by(id=user_id).first()

    if user == None:
        response = Response(status_code=302)
        response.headers["location"] = "/signin"
        return response

    template = views.get_template("/show.html")
    html = template.render(user=user)
    return HTMLResponse(html)

@users_router.get("/profile/edit")
def users_edit(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user-id")
    user = db.query(User).filter_by(id=user_id).first()

    if user == None:
        response = Response(status_code=302)
        response.headers["location"] = "/signin"
        return response

    template = views.get_template("/edit.html")
    html = template.render(user=user)
    return HTMLResponse(html)

@users_router.put("/profile")
async def users_update(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user-id")
    user = db.query(User).filter_by(id=user_id).first()

    if user == None:
        response = Response(status_code=302)
        response.headers["location"] = "/signin"
        return response

    form = await request.form()
    user.email = form["email"]
    user.hashed_password = bcrypt.hashpw(form["password"].encode("utf-8"), bcrypt.gensalt())
    db.add(user)
    db.commit()

    response = Response(status_code=303)
    response.headers["location"] = "/"
    return response

@users_router.delete("/profile")
def users_delete(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user-id")
    user = db.query(User).filter_by(id=user_id).first()

    if user == None:
        response = Response(status_code=302)
        response.headers["location"] = "/signin"
        return response

    db.delete(user)
    db.commit()

    response = Response(status_code=303)
    response.headers["location"] = "/"
    return response
