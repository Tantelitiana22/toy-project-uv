import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_product(async_client: AsyncClient):
    # WHEN
    response = await async_client.post("/products",
                                       json={"name": "test", "price": 10.45, "description": "test"})

    # THEN
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "test"
    assert data["price"] == 10.45
    assert data["description"] == "test"
