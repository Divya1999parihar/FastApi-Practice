from fastapi import FastAPI, Depends, HTTPException
from models import Product, ProductUpdate, ProductCreate
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

    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products")
def add_product(product: ProductCreate, db:Session = Depends(get_db)):
    try:
        db_product= db.query(db_models.Product).filter(db_models.Product.name== product.name).first()
    except:
        raise HTTPException(status_code=400, detail="Product already exists")
    else:
        db.add(db_models.Product(**product.model_dump()))
        db.commit()
        db.refresh(db_product) 
        raise HTTPException(status_code=201, detail="Product added successfully")

@app.put("/products")
def update_product(id:int, product:ProductUpdate, db:Session = Depends(get_db)):
    try:
        db_product= db.query(db_models.Product).filter(db_models.Product.id == id).first()
        if db_product:
            if product.name is not None:
                db_product.name = product.name
            if product.description is not None:
                db_product.description = product.description
            if product.price is not None:
                db_product.price = product.price
            if product.quantity is not None:
                db_product.quantity = product.quantity
        db.commit()
        return {"message": "Product updated successfully"}
    except:
        raise HTTPException(status_code=404, detail="Product not found")


@app.delete("/products")
def delete_product(id:int, db:Session = Depends(get_db)):
    try:
        db_product= db.query(db_models.Product).filter(db_models.Product.id == id).first()
        if db_product:
         db.delete(db_product)
        db.commit()
        return "product deleted successfully"
    except:
        raise HTTPException(status_code=404, detail="Product not found")
        
        