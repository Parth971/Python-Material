import pathlib
from time import sleep

import uvicorn
from fastapi import Depends, FastAPI, BackgroundTasks
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles

from app.dependencies import get_query_token, get_token_header
from app.internal import admin
from app.routers import items, users

BASE_DIR = pathlib.Path(__file__).parent.resolve()

app = FastAPI(dependencies=[Depends(get_query_token)])

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    items.router,
    prefix='/v1'
)
app.include_router(
    admin.router,
    prefix="/custom-admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


# def write_notification(email: str, message=""):
#     with open("log.txt", mode="w") as email_file:
#         sleep(5)
#         content = f"notification for {email}: {message}"
#         email_file.write(content)
#
#
# @app.post("/send-notification/{email}")
# async def send_notification(email: str, background_tasks: BackgroundTasks):
#     background_tasks.add_task(write_notification, email, message="some notification")
#     return {"message": "Notification sent in the background"}

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    # print(background_tasks.__dict__)
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@app.post("/send-notification/{email}")
async def send_notification(
        email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}

# def use_route_names_as_operation_ids(app: FastAPI) -> None:
#     """
#     Simplify operation IDs so that generated API clients have simpler function
#     names.
#
#     Should be called only after all routes have been added.
#     """
#     for route in app.routes:
#         if isinstance(route, APIRoute):
#             route.operation_id = route.name  # in this case, 'read_items'
#
#
# use_route_names_as_operation_ids(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
