from typing import Optional, List
from models import ProductOut, ProductCreate, ProductUpdate
from repositories import ProductRepository

class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def create_product(self, data: ProductCreate) -> ProductOut:
        return self.repo.create(data.name, data.price, data.in_stock)

    def list_products(self, min_price: Optional[int] = None, max_price: Optional[int] = None, in_stock: Optional[bool] = None) -> List[ProductOut]:
        if min_price is not None and max_price is not None and min_price > max_price:
            raise ValueError("min_price cannot be greater than max_price")
            
        return self.repo.get_all(min_price, max_price, in_stock)

    def get_product(self, product_id: int) -> Optional[ProductOut]:
        return self.repo.get_by_id(product_id)

    def update_product(self, product_id: int, data: ProductUpdate) -> Optional[ProductOut]:
        existing = self.repo.get_by_id(product_id)
        
        if not existing:
            return None
            
        new_name = data.name if data.name is not None else existing.name
        new_price = data.price if data.price is not None else existing.price
        new_in_stock = data.in_stock if data.in_stock is not None else existing.in_stock
        
        return self.repo.update(product_id, new_name, new_price, new_in_stock)

    def delete_product(self, product_id: int) -> bool:
        return self.repo.delete(product_id)
