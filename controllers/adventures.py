from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, Response
from mako.lookup import TemplateLookup

from models.user import User
from models.adventure import Adventure
from sqlalchemy.orm import Session
from config.database import get_db
from controllers.common import get_user, redirect

adventures_router = APIRouter(prefix="/adventures")
views = TemplateLookup(directories=['views', 'views/adventure'])


@adventures_router.get("/")
def adventures_index(request: Request, db: Session = Depends(get_db)):
    user = get_user(request, db)
    if user is None:
        return redirect("/signin", 302)

    adventures = db.query(Adventure).filter_by(author=user).all()

    template = views.get_template("/index.html")
    html = template.render(user=user, adventures=adventures)
    return HTMLResponse(html)


@adventures_router.get("/new")
def adventures_new(request: Request, db: Session = Depends(get_db)):
    user = get_user(request, db)
    if user is None:
        return redirect("/signin", 302)

    template = views.get_template("/new.html")
    html = template.render(user=user)
    return HTMLResponse(html)


@adventures_router.post("/")
async def adventures_create(request: Request, db: Session = Depends(get_db)):
    user = get_user(request, db)
    if user is None:
        return redirect("/signin", 302)

    form = await request.form()
    adventure = Adventure(
        author=user,
        title=form["title"],
        description=form["description"],
        draft=("draft" in form)
    )
    db.add(adventure)
    db.commit()

    return redirect("/adventures/", 303)


@adventures_router.get("/{id}")
def adventures_read(id: int, request: Request, db: Session = Depends(get_db)):
    user = get_user(request, db)
    if user is None:
        return redirect("/signin", 302)

    adventure = db.query(Adventure).filter_by(id=id).first()
    if adventure is None or adventure.author_id != user.id:
        return redirect("/adventures/", 302)

    template = views.get_template("/show.html")
    html = template.render(user=user, adventure=adventure)
    return HTMLResponse(html)


@adventures_router.get("/{id}/edit")
def adventures_edit(id: int, request: Request, db: Session = Depends(get_db)):
    user = get_user(request, db)
    if user is None:
        return redirect("/signin", 302)

    adventure = db.query(Adventure).filter_by(id=id).first()
    if adventure is None or adventure.author_id != user.id:
        return redirect("/adventures/", 302)

    template = views.get_template("/edit.html")
    html = template.render(user=user, adventure=adventure)
    return HTMLResponse(html)


@adventures_router.put("/{id}")
async def adventures_update(id: int,
                             request: Request,
                             db: Session = Depends(get_db)):
    user = get_user(request, db)
    if user is None:
        return redirect("/signin", 302)

    adventure = db.query(Adventure).filter_by(id=id).first()
    if adventure is None or adventure.author_id != user.id:
        return redirect("/adventures/", 302)

    form = await request.form()
    adventure.title = form["title"]
    adventure.description = form["description"]
    adventure.draft = ("draft" in form)
    db.commit()

    return redirect("/adventures/", 303)


@adventures_router.delete("/{id}")
def adventures_delete(id: int,
                       request: Request,
                       db: Session = Depends(get_db)):
    user = get_user(request, db)
    if user is None:
        return redirect("/signin", 302)

    adventure = db.query(Adventure).filter_by(id=id).first()
    if adventure is None or adventure.author_id != user.id:
        return redirect("/adventures/", 302)

    db.delete(adventure)
    db.commit()

    return redirect("/adventures/", 303)
