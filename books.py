from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import json

app = FastAPI()

class BookUpdate(BaseModel):
    book_name: Optional[str] = None
    author_name: Optional[str] = None
    price: Optional[float] =None

class BookCreate(BaseModel):
    book_name: Optional[str] = None
    author_name: Optional[str]= None
    price: Optional[float] =None

with open("book.json", "r") as file:
    books = json.load(file)


@app.get("/")
def read_root():
    return "Welcome To Books World"


@app.get("/Book_ID/{Book_ID}")
def read_book_id(Book_ID: int):

    for book in books:
        if book["Book_ID"] == Book_ID:
            return {
                "Book_ID": Book_ID,
                "message": "Book found",
                "book": book
            }

    return {
        "message": "Book is Not Found"
    }


@app.put("/Book_ID/{Book_ID}")
def update(Book_ID: int, updated_book: BookUpdate):

    for book in books:

        if book["Book_ID"] == Book_ID:

            if updated_book.book_name is not None:
                book["book_name"] = updated_book.book_name

            if updated_book.author_name is not None:
                book["author_name"] = updated_book.author_name

            if updated_book.price is not None:
                book["price"] = updated_book.price

            with open("book.json", "w") as file:
                json.dump(books, file, indent=4)

            return {
                "message": "Book is updated",
                "book": book
            }

    return {"message": "Book not found"}


@app.post("/books")
def add_book(new_book: BookCreate):

    for book in books:
        if (
            book["book_name"] == new_book.book_name
            and book["author_name"] == new_book.author_name
            and book["price"] == new_book.price
        ):
            return {
                "message": "Book already exists",
                "book": book
            }

    if books:
        new_id = max(book["Book_ID"] for book in books) + 1
    else:
        new_id = 1

    book_data = {
        "Book_ID": new_id,
        "book_name": new_book.book_name,
        "author_name": new_book.author_name,
        "price": new_book.price
    }

    books.append(book_data)

    with open("book.json", "w") as file:
        json.dump(books, file, indent=4)

    return {
        "message": "New book added",
        "book": book_data
    }


    
@app.delete("/Book_ID/{Book_ID}")
def delete_book(Book_ID: int):
    for i, book in enumerate(books):
        if book["Book_ID"] == Book_ID:
            del books[i]
            
            # Save to JSON file
            with open("book.json", "w") as file:
                json.dump(books, file, indent=4)
            
            return {"message": f"Book {Book_ID} deleted"}
    return {"message": "Book not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)