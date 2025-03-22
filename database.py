import time

# Simple dictionary to store tasks (task_name: time)
tasks = {}

def add_task(task_name, task_time):
    """Adds a task with the given name and time."""
    tasks[task_name] = task_time

def check_due_tasks():
    """Checks if any task is due and returns it."""
    current_time = time.strftime("%H:%M")  # Get current time in HH:MM format
    for task_name, task_time in tasks.items():
        if task_time == current_time:
            return {"name": task_name, "time": task_time}
    return None  # No task due
