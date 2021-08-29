from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response
from mako.lookup import TemplateLookup

from models.adventure import Adventure
from config.database import Session

adventures_router = APIRouter(prefix="/adventures")
views = TemplateLookup(directories=['views', 'views/adventure'])

@adventures_router.get("/")
def adventures_index(q:Optional[str] = None):
    session = Session()
    adventures = session.query(Adventure).all()
    #TODO add filter if q exists

    template = views.get_template("/index.html")
    html = template.render(adventures=adventures)
    return HTMLResponse(html)

@adventures_router.get("/new")
def adventures_new():
    template = views.get_template("/new.html")
    html = template.render()
    return HTMLResponse(html)

@adventures_router.post("/")
async def adventures_create(request: Request):
    form = await request.form()
    adventure = Adventure(
            title=form["title"],
            description=form["description"],
            draft=("draft" in form)
            )
    session = Session()
    session.add(adventure)
    session.commit()

    response = Response(status_code=303)
    response.headers["location"] = "/adventures/"
    return response


@adventures_router.get("/{id}")
def adventures_read(id:int):
    session = Session()
    adventure = session.query(Adventure).filter_by(id=id).first()

    template = views.get_template("/show.html")
    html = template.render(adventure=adventure)
    return HTMLResponse(html)

@adventures_router.get("/{id}/edit")
def adventures_edit(id:int):
    session = Session()
    adventure = session.query(Adventure).filter_by(id=id).first()

    template = views.get_template("/edit.html")
    html = template.render(adventure=adventure)
    return HTMLResponse(html)

@adventures_router.put("/{id}")
async def adventures_update(id: int, request: Request):
    form = await request.form()
    session = Session()
    adventure = session.query(Adventure).filter_by(id=id).first()
    adventure.title = form["title"]
    adventure.description = form["description"]
    adventure.draft = ("draft" in form)
    session.add(adventure)
    session.commit()

    response = Response(status_code=303)
    response.headers["location"] = "/adventures/"
    return response

@adventures_router.delete("/{id}")
def adventures_delete(id: int):
    session = Session()
    adventure = session.query(Adventure).filter_by(id=id).first()
    session.delete(adventure)
    session.commit()

    response = Response(status_code=303)
    response.headers["location"] = "/adventures/"
    return response
