from typing import Dict, List

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from toy_project.models.product import Product

class ProductController:
    @staticmethod
    async def register_product(product_dict: Dict, async_session: AsyncSession)-> Dict:
        product = Product(**product_dict)
        async_session.add(product)
        await async_session.commit()
        await async_session.refresh(product)
        return {**product_dict, "id": product.id}

    @staticmethod
    async def get_product_list(async_session: AsyncSession) -> List[Dict]:
        query = select(Product)
        products = await async_session.exec(query)
        return list(products.fetchall())

    @staticmethod
    async def get_product_by_id(id_product: int, async_session: AsyncSession) -> Dict:
        query = select(Product).where(Product.id == id_product)
        product = await async_session.exec(query)
        return product.first()
