from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions import ItemNotFoundError
from app.routers.items import router

app = FastAPI(title="Items API")

app.include_router(router)

@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(
        request: Request,
        exc: ItemNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )
