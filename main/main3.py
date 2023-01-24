from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import strawberry
from strawberry.asgi import GraphQL


app = FastAPI()


@strawberry.type
class User:
    name: str
    desc: str


@strawberry.type
class Query:
    @strawberry.field
    def user(self) -> User:
        return User(name="Patrick", age=100)


schema = strawberry.Schema(query=Query)
graphql_app = GraphQL(schema)


@app.get("/app/")
def read_app():
    return {"key": "app"}


app.mount("/static", StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


@app.get('/items/{item_id}', response_class=HTMLResponse)
async def read_static(request: Request, item_id: int):
    return templates.TemplateResponse("item.html", {"request": request, "id": item_id})

app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

sub = FastAPI()


@sub.get("/sub/")
def read_sub():
    return {"key": "sub"}


app.mount('/subapi/', sub)
