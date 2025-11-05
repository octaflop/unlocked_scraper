---
marp: true
title: Python Web Development Journey
theme: gaia
paginate: true
---

# Python Web Development Journey
## From Static Sites to Dynamic Applications

- A 3-act workshop exploring web development with Python
- ![](./workshop_qr.png)

---

# Act 1: Getting Started with Web Basics 🌐

<!-- eta: 15min -->

## Understanding Static Web Hosting

- Basic HTML/CSS structure
- Python's `http.server` for local development
- Deploying static sites

---

# Your First Python Web Server 🚀

```python
from http.server import HTTPServer, SimpleHTTPRequestHandler

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Serving at port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
```

---

# Act 2: Enter FastAPI ⚡

<!-- eta: 20min -->

## Moving to Modern Web Frameworks

- Introduction to FastAPI
- RESTful API concepts
- Request/Response cycle
- Path operations and routing

---

# Basic FastAPI Application

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    email: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/users/")
def create_user(user: User):
    return user
```

---

# Understanding Templates 📝

<!-- eta: 15min -->

## Why Templates Matter

- Separation of concerns
- Dynamic content generation
- Template syntax basics
- Introduction to Jinja2

---

# Act 3: Building Dynamic Applications 🎭

<!-- eta: 25min -->

## The Power of Jinja2 with FastAPI

- Template inheritance
- Dynamic data rendering
- HTMX integration
- Real-world patterns

---

# Demo: Jinja2 Templates in Action

```python
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fasthx import Jinja

app = FastAPI()
templates = Jinja2Templates(directory="templates")
jinja = Jinja(templates)

@app.get("/")
@jinja.page("index.html")
def index():
    return {"message": "Welcome!"}
```

---

# Building Our User List App 📋

```python
@app.get("/user-list")
@jinja.hx("user-list.html")
def htmx_or_data(response: Response) -> tuple[User, ...]:
    return (
        User(first_name="Alice", last_name="Johnson"),
        User(first_name="Bob", last_name="Smith"),
    )
```

---

# Template Structure

```html
{% extends 'base.html' %}
{% block content %}
    {% for user in items %}
        {{ user.first_name }} {{ user.last_name }}
    {% endfor %}
{% endblock %}
```

---

# Best Practices & Next Steps 🎯

- Structure matters: Keep templates organized
- Use template inheritance effectively
- Implement proper error handling
- Consider caching strategies
- Explore HTMX for enhanced interactivity

---

# Resources 📚

## Learning Materials

- FastAPI Documentation: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- Jinja2 Documentation: [jinja.palletsprojects.com](https://jinja.palletsprojects.com)
- HTMX: [htmx.org](https://htmx.org)

---

# Workshop Repository

- [Your Repository Link]
- Contains all examples and additional resources
- ![](./repo_qr.png)