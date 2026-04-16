from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Optional, List
from models import ProductCreate, ProductUpdate, ProductOut
from repositories import ProductRepository
from services import ProductService

router = APIRouter(prefix="/products", tags=["products"])

def get_service():
    repo = ProductRepository()
    return ProductService(repo)

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, service: ProductService = Depends(get_service)):
    return service.create_product(payload)

@router.get("/", response_model=List[ProductOut])
def list_products(
    min_price: Optional[int] = Query(None, ge=0),
    max_price: Optional[int] = Query(None, ge=0),
    in_stock: Optional[bool] = Query(None),
    service: ProductService = Depends(get_service)
):
    try:
        return service.list_products(min_price, max_price, in_stock)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, service: ProductService = Depends(get_service)):
    product = service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductUpdate, service: ProductService = Depends(get_service)):
    updated = service.update_product(product_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, service: ProductService = Depends(get_service)):
    deleted = service.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
