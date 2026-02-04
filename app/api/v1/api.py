from fastapi import APIRouter
from app.api.v1.endpoints import ingestion, chat, auth, budgets, dashboard

api_router = APIRouter()

api_router.include_router(ingestion.router, prefix="/documents", tags=["documents"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
