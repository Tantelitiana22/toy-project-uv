from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from toy_project.controller.product import ProductController
from toy_project.db import get_async_session


def get_product_controller(async_session: AsyncSession = Depends(get_async_session)) -> ProductController:
    return ProductController(async_session)
