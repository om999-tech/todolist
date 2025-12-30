# from api.dbConnection.connection import get_connection

# def create_task(data):
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)

#     query = """
#     INSERT INTO tasks (title, description, due_date, status)
#     VALUES (%s, %s, %s, %s)
#     """
#     cursor.execute(query, (
#         data["title"],
#         data.get("description"),
#         data.get("due_date"),
#         data.get("status")
#     ))
#     conn.commit()
#     task_id = cursor.lastrowid

#     cursor.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
#     task = cursor.fetchone()

#     cursor.close()
#     conn.close()
#     return task

# def get_tasks():
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)

#     cursor.execute("SELECT * FROM tasks")
#     tasks = cursor.fetchall()

#     cursor.close()
#     conn.close()
#     return tasks
