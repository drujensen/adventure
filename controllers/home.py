from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from mako.template import Template
from mako.lookup import TemplateLookup

home_router = APIRouter()
views = TemplateLookup(directories=['views'])

@home_router.get("/")
def home(request: Request):
	template = views.get_template("/home/index.html")
	return HTMLResponse(template.render())
