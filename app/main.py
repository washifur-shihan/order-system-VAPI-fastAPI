# from fastapi import FastAPI
# from app.api.menu import router as menu_router
# from app.api.chat import router as chat_router
# from app.api.orders import router as orders_router
# from app.api.vapi import router as vapi_router
# from app.api.kb import router as kb_router

# app = FastAPI(title="Order System")

# @app.get("/")
# async def root():
#     return {"message": "Order system API is running"}

# @app.get("/health")
# async def health():
#     return {"ok": True}

# app.include_router(menu_router, prefix="/menu", tags=["menu"])
# app.include_router(chat_router, prefix="/chat", tags=["chat"])
# app.include_router(orders_router, prefix="/orders", tags=["orders"])
# app.include_router(vapi_router, prefix="/vapi", tags=["vapi"])
# app.include_router(kb_router, prefix="/kb", tags=["kb"])

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.menu import router as menu_router
from app.api.chat import router as chat_router
from app.api.orders import router as orders_router
from app.api.vapi import router as vapi_router
from app.api.kb import router as kb_router

app = FastAPI(title="Order System")

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="order.html",
        context={}
    )

@app.get("/health")
async def health():
    return {"ok": True}


app.include_router(menu_router, prefix="/menu", tags=["menu"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(orders_router, prefix="/orders", tags=["orders"])
app.include_router(vapi_router, prefix="/vapi", tags=["vapi"])

app.include_router(kb_router, prefix="/kb", tags=["kb"])