import pytest
from fastapi import status
from httpx import AsyncClient, Response


async def post_response(async_client: AsyncClient, base_rout_path: str) -> Response:
    return await async_client.post(
        f"{base_rout_path}/products",
        json={"name": "test", "price": 10.45, "description": "test"},
    )


@pytest.mark.asyncio
async def test_create_product(async_client: AsyncClient, base_rout_path: str):
    # WHEN
    response = await post_response(async_client, base_rout_path)
    data = response.json()
    # THEN
    assert response.status_code == status.HTTP_201_CREATED
    assert data["name"] == "test"
    assert data["price"] == 10.45
    assert data["description"] == "test"


@pytest.mark.asyncio
async def test_get_product(async_client: AsyncClient, base_rout_path: str):
    # WHEN
    post_res = await post_response(async_client, base_rout_path)
    product_id = post_res.json()["id"]
    response = await async_client.get(f"{base_rout_path}/products/{product_id}")
    data = response.json()
    # THEN
    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == "test"
    assert data["price"] == 10.45
    assert data["description"] == "test"


@pytest.mark.asyncio
async def test_exception_get_product(async_client: AsyncClient, base_rout_path: str):
    # GIVEN
    no_existing_product_id = 834
    # WHEN
    response = await async_client.get(f"{base_rout_path}/products/{no_existing_product_id}")
    data = response.json()
    # THEN
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data["detail"] == f"Product with id {no_existing_product_id} not found"


@pytest.mark.asyncio
async def test_get_products(async_client: AsyncClient, base_rout_path: str):
    # GIVEN
    data = [
        {"name": "test1", "price": 10.45, "description": "test1"},
        {"name": "test2", "price": 20.45, "description": "test2"},
    ]
    for product in data:
        await async_client.post(f"{base_rout_path}/products", json=product)
    # WHEN
    response = await async_client.get(f"{base_rout_path}/products")
    result = response.json()
    # THEN
    assert response.status_code == status.HTTP_200_OK
    for i, product in enumerate(data):
        assert product["name"] == result[i]["name"]
        assert product["price"] == result[i]["price"]
        assert product["description"] == result[i]["description"]


@pytest.mark.asyncio
async def test_delete_product(async_client: AsyncClient, base_rout_path: str):
    # WHEN
    post_res = await post_response(async_client, base_rout_path)
    product_id = post_res.json()["id"]
    response = await async_client.delete(f"{base_rout_path}/products/{product_id}")
    data = response.json()
    # THEN
    assert response.status_code == status.HTTP_200_OK
    assert data["detail"] == f"Product with id {product_id} deleted successfully"


@pytest.mark.asyncio
async def test_put_product(async_client: AsyncClient, base_rout_path: str):
    # GIVEN
    data_update = {"name": "run_test", "price": 8.5}
    # WHEN
    post_res = await post_response(async_client, base_rout_path)
    json_data = post_res.json()
    product_id = json_data["id"]
    initial_description = json_data["description"]
    response = await async_client \
        .put(f"{base_rout_path}/products/{product_id}",
             json=data_update
             )
    data = response.json()
    # THEN
    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == data_update["name"]
    assert data["price"] == data_update["price"]
    assert data["description"] == initial_description
