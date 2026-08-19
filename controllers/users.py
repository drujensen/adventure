from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, Response
from mako.lookup import TemplateLookup

from models.user import User
from sqlalchemy.orm import Session
from config.database import get_db
from controllers.common import get_user, redirect, login, logout
import bcrypt


def _hash(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


users_router = APIRouter()
views = TemplateLookup(directories=['views', 'views/user'])


@users_router.get("/signup")
def users_new(request: Request, db: Session = Depends(get_db)):
    user = get_user(request, db)

    template = views.get_template("/new.html")
    html = template.render(user=user)
    return HTMLResponse(html)


@users_router.post("/profile")
async def users_create(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    email = form.get("email", "").strip()
    password = form.get("password", "")

    if not email or not password:
        return redirect("/signup", 303)

    existing = db.query(User).filter_by(email=email).first()
    if existing is not None:
        return redirect("/signup", 303)

    user = User(
            email=email,
            hashed_password=_hash(password)
            )
    db.add(user)
    db.commit()
    db.refresh(user)

    response = redirect("/", 303)
    login(response, user.id)
    return response


@users_router.get("/profile")
def users_read(request: Request, db: Session = Depends(get_db)):
    user = get_user(request, db)
    if user is None:
        return redirect("/signin", 302)

    template = views.get_template("/show.html")
    html = template.render(user=user)
    return HTMLResponse(html)


@users_router.get("/profile/edit")
def users_edit(request: Request, db: Session = Depends(get_db)):
    user = get_user(request, db)
    if user is None:
        return redirect("/signin", 302)

    template = views.get_template("/edit.html")
    html = template.render(user=user)
    return HTMLResponse(html)


@users_router.put("/profile")
async def users_update(request: Request, db: Session = Depends(get_db)):
    user = get_user(request, db)
    if user is None:
        return redirect("/signin", 302)

    form = await request.form()
    email = form.get("email", "").strip()
    password = form.get("password", "")

    if email:
        user.email = email
    if password:
        user.hashed_password = _hash(password)
    db.commit()

    return redirect("/", 303)


@users_router.delete("/profile")
def users_delete(request: Request, db: Session = Depends(get_db)):
    user = get_user(request, db)
    if user is None:
        return redirect("/signin", 302)

    db.delete(user)
    db.commit()

    response = redirect("/", 303)
    logout(response)
    return response
