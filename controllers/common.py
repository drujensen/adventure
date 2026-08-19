from typing import Optional

from fastapi import Request
from fastapi.responses import Response
from sqlalchemy.orm import Session

from models.user import User

USER_COOKIE = "user-id"


def get_user(request: Request, db: Session) -> Optional[User]:
    user_id = request.cookies.get(USER_COOKIE)
    if user_id is None:
        return None
    return db.query(User).filter_by(id=user_id).first()


def redirect(location: str, status_code: int = 303) -> Response:
    response = Response(status_code=status_code)
    response.headers["location"] = location
    return response


def login(response: Response, user_id: int) -> None:
    response.set_cookie(
        USER_COOKIE,
        str(user_id),
        httponly=True,
        samesite="lax",
    )


def logout(response: Response) -> None:
    response.set_cookie(USER_COOKIE, "", max_age=0)
