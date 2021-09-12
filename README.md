# Adventure

Adventure is an example server-side rendered web-based site using Python's FastAPI.  
It uses Mako templating and SqlAlchemy ORM for storage.  The basic site builds
a CRUD service to managing your adventures i.e. a blog site.

## Installation

Setup your virtual python environment:
```
python3 -m venv env
```
Activate the environment each time you start a new terminal:
```
. env/bin/activate
```

Install the packages:
```
pip install -r requirements.txt
```

## Run

To launch the application:
```
uvicorn main:app --reload
```
