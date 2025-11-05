import os
from typing import Optional

from sqlmodel import Field, SQLModel
from fastapi import FastAPI, Response
from fastapi.templating import Jinja2Templates

from fasthx import Jinja


# Pydantic model of the data the example API is using.
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    age: Optional[int] = None


basedir = os.path.abspath(os.path.dirname(__file__))

# Create the app instance.
app = FastAPI()

# Create a FastAPI Jinja2Templates instance. This will be used in FastHX Jinja instance.
templates = Jinja2Templates(directory=os.path.join(basedir, "templates"))

# FastHX Jinja instance is initialized with the Jinja2Templates instance.
jinja = Jinja(templates)


@app.get("/user-list")
@jinja.hx("user-list.html")  # Render the response with the user-list.html template.
def htmx_or_data(response: Response) -> tuple[User, ...]:
    """This route can serve both JSON and HTML, depending on if the request is an HTMX request or not."""
    response.headers["my-response-header"] = "works"

    return (
        User(first_name="Peter", last_name="Volf", age=18),
        User(
            first_name="John",
            last_name="Doe",
            age=20,
        ),
        User(first_name="Hasan", last_name="Tasan", age=24),
    )


@app.get("/admin-list")
@jinja.hx("user-list.html", no_data=True)  # Render the response with the user-list.html template.
def htmx_only() -> list[User]:
    """This route can only serve HTML, because the no_data parameter is set to True."""
    return [User(first_name="John", last_name="Doe", age=10)]


@app.get("/")
@jinja.page("index.html")
def index() -> None:
    """This route serves the index.html template."""
    ...