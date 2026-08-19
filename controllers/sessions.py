from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, Response
from mako.lookup import TemplateLookup
import bcrypt

from models.user import User
from sqlalchemy.orm import Session
from config.database import get_db
from controllers.common import get_user, redirect, login, logout

sessions_router = APIRouter()
views = TemplateLookup(directories=['views', 'views/session'])


@sessions_router.get("/signin")
def sessions_new(request: Request, db: Session = Depends(get_db)):
    user = get_user(request, db)
    template = views.get_template("/new.html")
    html = template.render(user=user)
    return HTMLResponse(html)


@sessions_router.post("/session")
async def sessions_create(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    email = form["email"]
    password = form["password"]

    user = db.query(User).filter_by(email=email).first()

    if user is None:
        return redirect("/signin", 303)

    stored = user.hashed_password
    if isinstance(stored, bytes):
        stored_hash = stored
    else:
        stored_hash = stored.encode("utf-8")

    if not bcrypt.checkpw(password.encode("utf-8"), stored_hash):
        return redirect("/signin", 303)

    response = redirect("/", 303)
    login(response, user.id)
    return response


@sessions_router.delete("/signout")
def sessions_delete(request: Request):
    response = redirect("/", 303)
    logout(response)
    return response
