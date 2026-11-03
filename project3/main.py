from fastapi import FastAPI, Depends
from models import Product
from database import SessionLocal, engine
import db_models
from sqlalchemy.orm import Session

app= FastAPI()

db_models.Base.metadata.create_all(bind=engine)

products=[
    Product(id=1,name="phone",description="budget Phone", price=99.9, quantity=10),
    Product(id=2,name="laptop",description="gaming", price=999.8, quantity=6),
    Product(id=3,name="pen",description="A blue ink pen", price=9.9, quantity=15),
    Product(id=4,name="table",description="wooden table", price=159.8, quantity=19)
]

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def greet():
    return "Welcom to API"

def init_db():
    db= SessionLocal()
    count= db.query(db_models.Product).count()

    if count == 0:
        for product in products:
            db.add(db_models.Product(**product.model_dump()))

        db.commit()

init_db()

@app.get("/products")
def get_all_products(db:Session = Depends(get_db)):

    db_products= db.query(db_models.Product).all()

    return db_products

@app.get("/products/{id}")
def get_product_by_id(id:int, db:Session = Depends(get_db)):
    db_product= db.query(db_models.Product).filter(db_models.Product.id== id).first()
    if db_product:
        return db_product

    return "product not found"

@app.post("/products")
def add_product(product: Product, db:Session = Depends(get_db)):
    db_product= db.query(db_models.Product).filter(db_models.Product.id== product.id).first()
    if db_product:
        return "product already exists"

    db.add(db_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products")
def update_product(id:int, product:Product, db:Session = Depends(get_db)):
    db_product= db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "product updated successfully"
    else:
        return "Product not found"


@app.delete("/products")
def delete_product(id:int, db:Session = Depends(get_db)):
    db_product= db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "product deleted successfully"
    else:
        return "product not found"
        