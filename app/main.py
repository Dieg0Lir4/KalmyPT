from fastapi import FastAPI
from app.api.items import router as items_router
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Items API",
    description="API para gestionar items",
    version="1.0.0"
)

app.include_router(items_router)