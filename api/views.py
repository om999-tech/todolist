from fastapi import APIRouter,HTTPException,status
from api.models import Task,TaskCreate,TaskUpdate
import logging
from api.dbConnection.connection import get_connection
from api.core.customresponse import CustomResponse

router = APIRouter()
@router.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "INSERT INTO tasks (title, description, due_date, status) VALUES (%s,%s,%s,%s)"
        cursor.execute(query, (task.title, task.description, task.due_date, task.status))
        conn.commit()
        task_id = cursor.lastrowid

        cursor.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        # Convert MySQL dict to Pydantic Task model
        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            due_date=row["due_date"],
            status=row["status"]
        )

    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500, detail="Task creation failed")

@router.get("/tasks")
def list_tasks():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convert any date objects to ISO format strings
        for task in tasks:
            if task.get("due_date"):
                task["due_date"] = task["due_date"].isoformat()

        return CustomResponse(
            message="Tasks fetched successfully.",
            data=tasks,
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        print(str(e))
        return CustomResponse(
            message="Failed to fetch tasks.",
            data=[],
            status=status.HTTP_400_BAD_REQUEST,
        )

       

@router.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
        task = cursor.fetchone()
        cursor.close()
        conn.close()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch task")

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch existing task
        cursor.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
        existing_task = cursor.fetchone()
        if not existing_task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Convert TaskUpdate to dict, excluding unset fields
        update_data = task.dict(exclude_unset=True)

        for key, value in update_data.items():
            existing_task[key] = value

        # Build SQL query dynamically
        set_clause = ", ".join(f"{key}=%s" for key in update_data.keys())
        if set_clause:  # Only update if there's at least one field
            query = f"UPDATE tasks SET {set_clause} WHERE id=%s"
            values = list(update_data.values()) + [task_id]
            cursor.execute(query, values)
            conn.commit()

        # Return updated task
        cursor.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        return Task(**row)

    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500, detail="Failed to update task")

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Task not found")
        cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"detail": "Task deleted successfully"}
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500, detail="Failed to delete task")
