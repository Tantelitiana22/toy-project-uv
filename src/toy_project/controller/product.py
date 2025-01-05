from typing import Dict, List

from fastapi import HTTPException
from sqlalchemy.engine import TupleResult
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from toy_project.models.product import Product, ProductUpdate


class ProductController:
    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def register_product(self, product_dict: Dict) -> Dict:
        product = Product(**product_dict)
        self.async_session.add(product)
        await self.async_session.commit()
        await self.async_session.refresh(product)
        return {**product_dict, "id": product.id}

    async def get_product_list(self) -> List[Dict]:
        query = select(Product)
        products = await self.async_session.exec(query)
        return list(products.fetchall())

    async def _get_product_model_by_id(self, id_product: int) -> TupleResult[Product]:
        query = select(Product).where(Product.id == id_product)
        return await self.async_session.exec(query)

    async def get_product_by_id(self, id_product: int) -> Product:
        product = await self._get_product_model_by_id(id_product)
        one_product = product.one_or_none()
        if one_product is None:
            raise HTTPException(status_code=404, detail=f"Product with id {id_product} not found")
        return one_product

    async def delete_product_by_id(self, id_product: int) -> Dict[str, str]:
        product_first = await self.get_product_by_id(id_product)
        await self.async_session.delete(product_first)
        await self.async_session.commit()
        return {"detail": f"Product with id {id_product} deleted successfully"}

    async def update_product_by_id(self, product_id, product: ProductUpdate) -> Product:
        one_product = await self.get_product_by_id(product_id)
        product_dict = product.model_dump(exclude_unset=True)
        one_product.sqlmodel_update(product_dict)
        await self.async_session.commit()
        await self.async_session.refresh(one_product)
        return one_product
