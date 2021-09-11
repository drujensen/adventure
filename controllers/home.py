from models.adventure import Adventure
from fastapi import APIRouter
from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from mako.template import Template
from mako.lookup import TemplateLookup

from models.user import User
from models.adventure import Adventure
from sqlalchemy.orm import Session
from config.database import get_db

home_router = APIRouter()
views = TemplateLookup(directories=['views'])

@home_router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user-id")
    user = db.query(User).filter_by(id=user_id).first()

    adventures = db.query(Adventure).filter_by(draft=False).all()
    template = views.get_template("/home/index.html")
    return HTMLResponse(template.render(user=user, adventures=adventures))

@home_router.get("/details/{id}")
def details(id: int, request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user-id")
    user = db.query(User).filter_by(id=user_id).first()

    adventure = db.query(Adventure).filter_by(id=id).first()

    template = views.get_template("/home/show.html")
    html = template.render(user=user, adventure=adventure)
    return HTMLResponse(html)
