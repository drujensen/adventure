from fastapi import APIRouter
from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from mako.lookup import TemplateLookup

from models.user import User
from models.adventure import Adventure
from sqlalchemy.orm import Session
from config.database import get_db
from controllers.common import get_user

home_router = APIRouter()
views = TemplateLookup(directories=['views'])


@home_router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    user = get_user(request, db)

    adventures = db.query(Adventure).filter_by(draft=False).all()
    template = views.get_template("/home/index.html")
    return HTMLResponse(template.render(user=user, adventures=adventures))


@home_router.get("/about")
def about(request: Request, db: Session = Depends(get_db)):
    user = get_user(request, db)

    template = views.get_template("/home/about.html")
    return HTMLResponse(template.render(user=user))


@home_router.get("/details/{id}")
def details(id: int, request: Request, db: Session = Depends(get_db)):
    user = get_user(request, db)

    adventure = db.query(Adventure).filter_by(id=id).first()

    template = views.get_template("/home/show.html")
    html = template.render(user=user, adventure=adventure)
    return HTMLResponse(html)
