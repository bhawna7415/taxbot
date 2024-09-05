from pydantic import BaseModel
from typing import List, Optional


class Product(BaseModel):
    product_name: str
    product_description: str
    product_status: str
    product_category: str
    product_subcategory: str

class ProductToClassify(BaseModel):
    product_name: str
    product_description: str

class ClassificationRequest(BaseModel):
    existing_products: List[Product]
    product_to_classify: ProductToClassify
    
class ProductClassification(BaseModel):
    category: str
    subcategory: str

class ClassificationResponse(BaseModel):
    product_classification: ProductClassification