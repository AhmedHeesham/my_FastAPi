from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Union
from typing_extensions import Annotated

app = FastAPI()

# In-memory database (for demonstration purposes)
products_db = [
    {"id": 1, "name": "laptop", "price": 800},
    {"id": 2, "name": "mouse", "price": 20},
    {"id": 3, "name": "monitor", "price": 400},
]

@app.get("/")
async def root():
    # Return a simple message
    return {"message": "Welcome to my e-commerce API"}

@app.get("/products")
async def get_products():
    return {"products": products_db}

class Product(BaseModel):
    name: str = Field(title="Product name", min_length=3, max_length=25)
    price: float = Field(title="Product price", gt=0)  # gt is greater than
    description: Union[str, None] = None

@app.post("/products")
async def create_product(product: Product):
    # Generate a new ID
    new_id = len(products_db) + 1
    
    # Add the new product to the in-memory database
    new_product = {"id": new_id, "name": product.name, "price": product.price, "description": product.description}
    products_db.append(new_product)
    
    return {"message": "Product added successfully", "product": new_product}

def find_product_py_id(product_id):
    for product in products_db:
        if product["id"] == product_id:
            return product
    return None

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    product = find_product_py_id(product_id)
    if product:
        return {"product": product}
    return {"error": "Product not found"}

@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    # Find the product by ID
    product_to_update = find_product_py_id(product_id)
    if product_to_update:
        # Update the product
        product_to_update["name"] = product.name
        product_to_update["price"] = product.price
        product_to_update["description"] = product.description
        return {"message": "Product updated successfully", "product": product_to_update}
    return {"error": "Product not found"}

@app.get('/search')
async def search_product(search_query: Annotated[Union[str, None], Query(min_length=3)] = None, min_price: Annotated[Union[float, None], Query(gt=0)] = None):

    if search_query:
        search_results = [product for product in products_db if search_query.lower() in product["name"].lower()]
        if min_price:
            search_results = [product for product in search_results if product["price"] >= min_price]
    else:
        search_results = products_db
    return {"search_results": search_results}
        
@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    # Find the product by ID
    product_to_delete = find_product_py_id(product_id)
    if product_to_delete:
        # Delete the product
        products_db.remove(product_to_delete)
        return {"message": "Product deleted successfully"}
    return {"error": "Product not found"}
    
    
    
