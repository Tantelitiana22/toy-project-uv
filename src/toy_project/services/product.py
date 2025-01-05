from typing import List

from fastapi import APIRouter, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from toy_project.controller.product import ProductController
from toy_project.db import get_async_session
from toy_project.models.product import Product, ProductInput, ProductOutput

router = APIRouter(tags=["product"])


@router.get("/products", response_model=List[Product], status_code=status.HTTP_200_OK)
async def get_products(session: AsyncSession = Depends(get_async_session)):
    return await ProductController.get_product_list(session)


@router.get("/products/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
async def get_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    return await ProductController.get_product_by_id(product_id, session)


@router.post("/products", response_model=ProductOutput, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductInput, session: AsyncSession = Depends(get_async_session)):
    return await ProductController.register_product(product.model_dump(), session)
