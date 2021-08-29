from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, Response
from mako.lookup import TemplateLookup
from sqlalchemy import select

from controllers.dto.adventure import AdventureData
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

@adventures_router.post("/", response_model=AdventureData)
def adventures_create(adventure_data: AdventureData = Depends(AdventureData.as_form)):
    adventure = Adventure(
            title=adventure_data.title,
            description=adventure_data.description,
            draft=adventure_data.draft
            )
    session = Session()
    session.add(adventure)
    session.commit()

    response = Response(status_code=303)
    response.headers["location"] = "/adventures/"
    return response


@adventures_router.get("/{adventure_id}")
def adventures_read(adventure_id:int):
    session = Session()
    adventure = session.query(Adventure).filter_by(id=adventure_id).first()

    template = views.get_template("/show.html")
    html = template.render(adventure=adventure)
    return HTMLResponse(html)

@adventures_router.get("/{adventure_id}/edit")
def adventures_edit(adventure_id:int):
    session = Session()
    adventure = session.query(Adventure).filter_by(id=adventure_id).first()

    template = views.get_template("/edit.html")
    html = template.render(adventure=adventure)
    return HTMLResponse(html)

@adventures_router.post("/{adventure_id}", response_model=AdventureData)
def adventures_update(adventure_id: int, adventure_data: AdventureData = Depends(AdventureData.as_form)):
    session = Session()
    adventure = session.query(Adventure).filter_by(id=adventure_id).first()
    adventure.title = adventure_data.title
    adventure.description = adventure_data.description
    adventure.draft = adventure_data.draft
    session.add(adventure)
    session.commit()

    response = Response(status_code=303)
    response.headers["location"] = "/adventures/"
    return response

@adventures_router.get("/{adventure_id}/delete")
def adventures_delete(adventure_id: int):
    session = Session()
    adventure = session.query(Adventure).filter_by(id=adventure_id).first()
    session.delete(adventure)
    session.commit()

    response = Response(status_code=303)
    response.headers["location"] = "/adventures/"
    return response
