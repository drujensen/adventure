from typing import Optional

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, Response
from mako.lookup import TemplateLookup

from models.user import User
from models.adventure import Adventure
from sqlalchemy.orm import Session
from config.database import get_db

adventures_router = APIRouter(prefix="/adventures")
views = TemplateLookup(directories=['views', 'views/adventure'])

@adventures_router.get("/")
def adventures_index(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user-id")
    user = db.query(User).filter_by(id=user_id).first()

    if user == None:
        response = Response(status_code=302)
        response.headers["location"] = "/signin"
        return response

    adventures = db.query(Adventure).filter_by(author=user).all()

    template = views.get_template("/index.html")
    html = template.render(user=user, adventures=adventures)
    return HTMLResponse(html)

@adventures_router.get("/new")
def adventures_new(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user-id")
    user = db.query(User).filter_by(id=user_id).first()

    if user == None:
        response = Response(status_code=302)
        response.headers["location"] = "/signin"
        return response

    template = views.get_template("/new.html")
    html = template.render(user=user)
    return HTMLResponse(html)

@adventures_router.post("/")
async def adventures_create(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user-id")
    user = db.query(User).filter_by(id=user_id).first()

    if user == None:
        response = Response(status_code=302)
        response.headers["location"] = "/signin"
        return response

    form = await request.form()
    adventure = Adventure(
        author=user,
        title=form["title"],
        description=form["description"],
        draft=("draft" in form)
    )
    db.add(adventure)
    db.commit()

    response = Response(status_code=303)
    response.headers["location"] = "/adventures/"
    return response

@adventures_router.get("/{id}")
def adventures_read(id:int, request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user-id")
    user = db.query(User).filter_by(id=user_id).first()

    if user == None:
        response = Response(status_code=302)
        response.headers["location"] = "/signin"
        return response

    adventure = db.query(Adventure).filter_by(id=id).first()

    template = views.get_template("/show.html")
    html = template.render(user=user, adventure=adventure)
    return HTMLResponse(html)

@adventures_router.get("/{id}/edit")
def adventures_edit(id:int, request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user-id")
    user = db.query(User).filter_by(id=user_id).first()

    if user == None:
        response = Response(status_code=302)
        response.headers["location"] = "/signin"
        return response

    adventure = db.query(Adventure).filter_by(id=id).first()

    template = views.get_template("/edit.html")
    html = template.render(user=user, adventure=adventure)
    return HTMLResponse(html)

@adventures_router.put("/{id}")
async def adventures_update(id: int, request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user-id")
    user = db.query(User).filter_by(id=user_id).first()

    if user == None:
        response = Response(status_code=302)
        response.headers["location"] = "/signin"
        return response

    form = await request.form()

    adventure = db.query(Adventure).filter_by(id=id).first()
    adventure.author = user
    adventure.title = form["title"]
    adventure.description = form["description"]
    adventure.draft = ("draft" in form)
    db.add(adventure)
    db.commit()

    response = Response(status_code=303)
    response.headers["location"] = "/adventures/"
    return response

@adventures_router.delete("/{id}")
def adventures_delete(id: int, request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user-id")
    user = db.query(User).filter_by(id=user_id).first()

    if user == None:
        response = Response(status_code=302)
        response.headers["location"] = "/signin"
        return response

    adventure = db.query(Adventure).filter_by(id=id).first()
    db.delete(adventure)
    db.commit()

    response = Response(status_code=303)
    response.headers["location"] = "/adventures/"
    return response
