from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import UUID, uuid4

app = FastAPI()

# Модель Pydantic для задачи
class Task(BaseModel):
    id: UUID
    title: str
    description: str
    completed: bool

# Хранилище задач в памяти
tasks_db = []

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks_db

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: UUID):
    task = next((task for task in tasks_db if task.id == task_id), None)
    if task is not None:
        return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", response_model=Task)
async def add_task(task: Task):
    task.id = uuid4()
    tasks_db.append(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: UUID, task_update: Task):
    for task in tasks_db:
        if task.id == task_id:
            task.title = task_update.title
            task.description = task_update.description
            task.completed = task_update.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: UUID):
    global tasks_db
    tasks_db = [task for task in tasks_db if task.id != task_id]
    return {"message": "Task deleted"}