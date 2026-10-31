from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def read_item():
    return("Product_Catelog")

@app.get("/Product_category/{Product_category}")
def read_Product(product_category : str, q: str | None=None):
    return{"Product_category":product_category, "q":q}

@app.get("/products/Min_price/{Min_price}")
def read_min_price(Min_price : float, q: str | None=None):
    return{"Min_price":Min_price, "q":q}

@app.get("/products/Max_price/{Max_price}")
def read_max_price(Max_price : float, q: str | None=None):
    return{"Max_price":Max_price, "q":q}

@app.get("/products/price/{price}")
def sort_list(price:str ="asc"):
    product=[]
    if price=="product":
        return {sorted(price)}
    else:
        return {sorted(price, reverse=True)}

@app.get("/products/total/{total}")
def read_total():
    total=180
    return{"total":total}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

