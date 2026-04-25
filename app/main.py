
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.services.restaurants import get_restaurant_by_slug, build_widget_assistant_config
from app.api.menu import router as menu_router
from app.api.chat import router as chat_router
from app.api.orders import router as orders_router
from app.api.kb import router as kb_router

app = FastAPI(title="Order System")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")



@app.get("/r/{slug}")
async def restaurant_page(request: Request, slug: str):
    restaurant = get_restaurant_by_slug(slug)
    if not restaurant:
        return {"error": "Restaurant not found"}

    widget_assistant_json = build_widget_assistant_config(restaurant)

    return templates.TemplateResponse(
        request=request,
        name="order.html",
        context={
            "request": request,
            "restaurant": restaurant,
            "widget_assistant_json": widget_assistant_json
        }
    )


@app.get("/health")
async def health():
    return {"ok": True}


app.include_router(menu_router, prefix="/menu", tags=["menu"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(orders_router, prefix="/orders", tags=["orders"])
app.include_router(kb_router, prefix="/kb", tags=["kb"])