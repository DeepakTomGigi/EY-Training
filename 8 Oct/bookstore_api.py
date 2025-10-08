from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Pydantic model
class Book(BaseModel):
    id: int
    title: str
    author: str
    price: float
    in_stock: bool

# Step 3: In-memory list of books
books = [
    Book(id=1, title="Deep Learning", author="Ian Goodfellow", price=1200, in_stock=True),
    Book(id=2, title="Python Tricks", author="Dan Bader", price=700, in_stock=False),
    Book(id=3, title="Fluent Python", author="Luciano Ramalho", price=900, in_stock=True),
]


# Return only books where in_stock = True
@app.get("/books/available")
def available_books():
    return [book for book in books if book.in_stock]


# Return total number of books
@app.get("/books/count")
def count_books():
    return {"count": len(books)}

# Search books
@app.get("/books/search")
def search_books(author: str = None, max_price: float = None):
    results = books

    if author:
        results = [book for book in results if author.lower() in book.author.lower()]
    if max_price is not None:
        results = [book for book in results if book.price <= max_price]

    return results

# GET all books
@app.get("/books")
def get_books():
    return books

# GET book by id
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# ADD a new book
@app.post("/books")
def create_book(book: Book):
    for b in books:
        if b.id == book.id:
            raise HTTPException(status_code=400, detail="Book already exists")
    books.append(book)
    return book

# Update a book
@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    for i in range(len(books)):
        if books[i].id == book_id:
            books[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

# Delete a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for i in range(len(books)):
        if books[i].id == book_id:
            del books[i]
            return {"detail": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

