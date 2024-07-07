from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import Todo
from database import fetch_one_todo, fetch_all_todos, create_todo, update_todo, remove_todo

# Create FastAPI app instance
app = FastAPI()

from database import(
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    update_todo,
    remove_todo,
)
# Define CORS origins
origins = [
    "https://localhost:3000",  # Replace with your frontend URL
]

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],
)

# Define a simple GET endpoint
@app.get("/")
def read_root():
    return {"ping": "pong"}

# Endpoint to fetch all todos
@app.get("/api/todo", response_model=list[Todo])
async def get_todo():
    response = await fetch_all_todos()
    return response

# Endpoint to fetch todo by title
@app.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_id(title: str):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(status_code=404, detail=f"No todo item with title '{title}'")

# Endpoint to create a new todo
@app.post("/api/todo", response_model=Todo)
async def post_todo(todo: Todo):
    response = await create_todo(todo)
    return response

# Endpoint to update todo by title
@app.put("/api/todo/{title}", response_model=Todo)
async def put_todo(title: str, desc: str):
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(status_code=404, detail=f"No todo item with title '{title}'")

# Endpoint to delete todo by title
@app.delete("/api/todo/{title}")
async def delete_todo(title: str):
    response = await remove_todo(title)
    if response:
        return {"message": f"Successfully deleted todo item with title '{title}'"}
    raise HTTPException(status_code=404, detail=f"No todo item with title '{title}'")
