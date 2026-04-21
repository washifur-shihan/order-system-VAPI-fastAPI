from fastapi import FastAPI
from app.api.menu import router as menu_router
from app.api.chat import router as chat_router
from app.api.orders import router as orders_router
from app.api.vapi import router as vapi_router

app = FastAPI(title="Order System")

@app.get("/")
async def root():
    return {"message": "Order system API is running"}

@app.get("/health")
async def health():
    return {"ok": True}

app.include_router(menu_router, prefix="/menu", tags=["menu"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(orders_router, prefix="/orders", tags=["orders"])
app.include_router(vapi_router, prefix="/vapi", tags=["vapi"])