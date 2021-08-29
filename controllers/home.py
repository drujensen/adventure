from models.adventure import Adventure
from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from mako.template import Template
from mako.lookup import TemplateLookup
from models.adventure import Adventure
from config.database import Session

home_router = APIRouter()
views = TemplateLookup(directories=['views'])

@home_router.get("/")
def home(request: Request):
    session = Session()
    adventures = session.query(Adventure).all()
    template = views.get_template("/home/index.html")
    return HTMLResponse(template.render(adventures=adventures))
