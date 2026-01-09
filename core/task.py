# core/task.py
from core.enums import TaskStatus, TaskPriority

class Task:
    def __init__(self, task_id, title, priority: TaskPriority, parent_id=None):
        self.id = task_id 
        self.title = title
        self.priority = priority # Agora espera um TaskPriority
        self.status = TaskStatus.BACKLOG 
        self.dependencies = set()
        self.subtasks = [] 
        self.parent_id = parent_id

    def __repr__(self):
        tipo = f"Subtask de {self.parent_id}" if self.parent_id else "Main Task"
        return (f"Task(id={self.id}, title='{self.title}', "
                f"status={self.status.name}, priority={self.priority.name}, "
                f"{tipo}, subtasks={len(self.subtasks)})")