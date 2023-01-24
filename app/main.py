from fastapi import Depends, FastAPI
from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users


description = """
## TITLE
* **App ot boga**
made in Valentina Budko!🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
"""
app = FastAPI(dependencies=[Depends(get_query_token)],
              title='Appp',
              description=description,
              version="0.0.1",
              terms_of_service="http://example.com/terms/",
              contact={
                  "name": "Deadpoolio the Amazing",
                  "url": "http://x-force.example.com/contact/",
                  "email": "dp@x-force.example.com",
              },
              license_info={
                  "name": "Apache 2.0",
                  "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
              })

app.include_router(users.router)
app.include_router(items.router)

app.include_router(admin.router, prefix='/admin', tags=["admin"],
                   responses={418: {"description": "teapot"}})


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}