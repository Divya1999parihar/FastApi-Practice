from fastapi import FastAPI
from models import Product

app= FastAPI()

products=[
    Product(id=1,name="phone",description="budget Phone", price=99.9, quantity=10),
    Product(id=2,name="laptop",description="gaming", price=999.8, quantity=6),
    Product(id=3,name="pen",description="A blue ink pen", price=9.9, quantity=15),
    Product(id=4,name="table",description="wooden table", price=159.8, quantity=19)
]


@app.get("/")
def greet():
    return "Welcom to API"

@app.get("/products")
def get_all_products():
    return products

@app.get("/products/{id}")
def get_product_by_id(id:int):
    for n in products:
        if n.id == id:
            return n

    return "product not found"

@app.post("/products")
def add_product(product: Product):
    for n in products:
        if n.id == product.id:
            return "product already Exits"

    products.append(product)
    return product

@app.put("/products")
def update_product(id:int, product:Product):
    for i in range(len(products)):
            if products[i].id == id:
                products[i]= product
                return "Product added successfully"

    return "Product not found"


@app.delete("/products")
def delete_product(id:int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "product is deleted"
    return "product not found"
        