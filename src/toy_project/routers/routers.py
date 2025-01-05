from fastapi import APIRouter

from toy_project.services.product import product_router

main_router = APIRouter(prefix="/api/v1")

main_router.include_router(product_router, tags=["product"])
