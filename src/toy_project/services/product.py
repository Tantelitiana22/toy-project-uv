from typing import List

from fastapi import APIRouter, status, Depends

from toy_project.controller.product import ProductController
from toy_project.dependencies.product import get_product_controller
from toy_project.models.product import Product, ProductInput, ProductOutput, ProductUpdate

product_router = APIRouter(tags=["product"])


@product_router.get("/products", response_model=List[Product], status_code=status.HTTP_200_OK)
async def get_products(product_controller: ProductController = Depends(get_product_controller)):
    return await product_controller.get_product_list()


@product_router.get("/products/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
async def get_product(product_id: int, product_controller: ProductController = Depends(get_product_controller)):
    return await product_controller.get_product_by_id(product_id)


@product_router.post("/products", response_model=ProductOutput, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductInput,
                         product_controller: ProductController = Depends(get_product_controller)):
    return await product_controller.register_product(product.model_dump())


@product_router.delete("/products/{product_id}", status_code=status.HTTP_200_OK, tags=["delete_product"])
async def delete_product(product_id: int, product_controller: ProductController = Depends(get_product_controller)):
    return await product_controller.delete_product_by_id(product_id)


@product_router.put("/products/{product_id}", response_model=ProductOutput, status_code=status.HTTP_200_OK)
async def update_product(product_id: int, product: ProductUpdate,
                         product_controller: ProductController = Depends(get_product_controller)):
    return await product_controller.update_product_by_id(product_id, product)
