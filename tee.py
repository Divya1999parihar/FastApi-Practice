from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()
# Define the Todo model
class Todo(BaseModel):
    id: int
    task: str
    completed: bool = False

# In-memory storage
todos = []

# Core operations
def create_todo(todo: Todo):
    todos.append(todo)
    return {"message": "Todo added!", "todo": todo}

def get_todos():
    return todos

def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return {"error": "Todo not found"}

def update_todo(todo_id: int, updated_todo: Todo):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[i] = updated_todo
            return {"message": "Todo updated!", "todo": updated_todo}
    return {"error": "Todo not found"}

def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(i)
            return {"message": "Todo deleted!"}
    return {"error": "Todo not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)


