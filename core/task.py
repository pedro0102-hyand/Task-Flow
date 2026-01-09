from core.enums import TaskStatus

class Task:

    def __init__(self, task_id, title, priority, parent_id=None):
        self.id = task_id  # Chave identificadora única
        self.title = title
        self.priority = priority
        self.status = TaskStatus.BACKLOG  # Status inicial
        self.dependencies = set()         # IDs de tarefas das quais esta depende
        self.subtasks = []                # Lista de objetos Task (filhos)
        self.parent_id = parent_id        # Referência ao ID da tarefa pai

    def __repr__(self):

        tipo = f"Subtask de {self.parent_id}" if self.parent_id else "Main Task"
        
        return (f"Task(id={self.id}, title='{self.title}', "
                f"status={self.status.name}, {tipo}, "
                f"subtasks={len(self.subtasks)})")