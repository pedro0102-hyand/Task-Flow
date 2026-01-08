from core.task import Task
from core.enums import TaskStatus
from structures.task_queue import TaskQueue
from structures.task_registry import TaskRegistry
from services.workflow_service import WorkflowService
from services.history_service import HistoryService
from algorithms.dependency_graph import DependencyGraph
from algorithms.sorting import sort_by_priority
from utils.id_generator import generate_id

# define e centraliza regras do sistema
class TaskService:

    def __init__(self):

        self.registry = TaskRegistry() # dicionario de registro das tarefas
        self.queue = TaskQueue() # fila de execucao
        self.workflow = WorkflowService()
        self.history = HistoryService()
        self.dependencies = DependencyGraph()

    def create_task(self, title, priority):

        task = Task(generate_id(), title, priority)
        self.registry.add(task)

        def undo():
            del self.registry.tasks[task.id] # remove task

        self.history.record(undo)
        return task

    def add_dependency(self, task_id, depends_on_id):

        self.dependencies.add_dependency(task_id, depends_on_id)

        if self.dependencies.has_cycle():
            raise Exception("Dependência cíclica detectada!")

        self.registry.get(task_id).dependencies.add(depends_on_id)

    def start_task(self):

        tasks = sort_by_priority(self.registry.all_tasks())

        for task in tasks:

            if self.workflow.can_start(task):

                task.status = TaskStatus.IN_PROGRESS
                self.queue.enqueue(task)


                def undo():
                    
                    # reverter o estado atual
                    task.status = TaskStatus.BACKLOG

                # registrar o estado
                self.history.record(undo)
                print(f"Iniciando {task}")
                return

    def finish_task(self):

        task = self.queue.dequeue() # remove task da fila

        # proteger contra erros de estado
        if not task or not self.workflow.can_finish(task):
            return

        # definindo como concluido
        task.status = TaskStatus.DONE

        def undo():

            # volta e reinsere na fila
            task.status = TaskStatus.IN_PROGRESS
            self.queue.enqueue(task)

        self.history.record(undo)
        print(f"Finalizando {task}")

    def undo_last_action(self):

        self.history.undo()
