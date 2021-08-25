from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


home_router = APIRouter()
views = Jinja2Templates(directory="views")


@home_router.get("/")
async def home(request: Request):
	return views.TemplateResponse("home/index.html",{"request":request})

