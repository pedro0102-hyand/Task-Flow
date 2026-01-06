from core.enums import TaskStatus

class Task:

    def __init__(self, task_id, title, priority):

        self.id = id # chave no dicionario
        self.title = title
        self.priority = priority
        self.status = TaskStatus.BACKLOG # status inicial no backlog
        self.dependencies = set()

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', status={self.status.name})"