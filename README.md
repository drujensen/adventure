# Adventure

Adventure is an example server-side rendered web-based site using Python's FastAPI.  
It uses Mako templating and SqlAlchemy ORM for storage.  The basic site builds
a CRUD service to managing your adventures i.e. a blog site.

## Installation

Setup your virtual python environment:
```
pipenv shell
```

Install the packages:
```
pipenv install
```

## Run

To launch the application:
```
uvicorn main:app --reload
```
