from typing import Annotated
from fastapi import FastAPI, Response, Cookie
from pickle import loads, dumps
from base64 import b64encode, b64decode
from pydantic import BaseModel
from enum import StrEnum
from pydantic_settings import BaseSettings
from random import choice


class Settings(BaseSettings):
    secret_key: str = "OVERRIDE SECRET_KEY ENV VAR"


class SessionType(StrEnum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class Session(BaseModel):
    user: str


def read_session(base64str: str) -> Session:
    try:
        return Session.model_validate(loads(b64decode(base64str)))
    except Exception:
        return Session(user=SessionType.GUEST)


def write_session(session: Session) -> str:
    return b64encode(dumps(session.model_dump())).decode()


sett = Settings()
app = FastAPI()


def random_pickle_fact():
    facts = [
        "Pickle Rick!",
        "I'm Pickle Rick!",
        "I turned myself into a pickle!",
        "Did you hear about the pickle factory fire?",
    ]

    return choice(facts)


@app.get("/")
def read_root(response: Response, ses_id: Annotated[str | None, Cookie()] = None):
    if ses_id:
        session = read_session(ses_id)
        if session.user == SessionType.ADMIN:
            return sett.secret_key
    else:
        new_ses = Session(user=SessionType.GUEST)
        response.set_cookie(key="ses_id", value=write_session(new_ses))
    return random_pickle_fact()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0")
