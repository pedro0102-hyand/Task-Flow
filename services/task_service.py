from core.task import Task
from core.enums import TaskStatus, TaskPriority
from structures.task_queue import TaskQueue
from structures.task_registry import TaskRegistry
from services.workflow_service import WorkflowService
from services.history_service import HistoryService
from algorithms.dependency_graph import DependencyGraph
from algorithms.sorting import sort_by_priority
from utils.id_generator import generate_id


class TaskService:

    def __init__(self):
        self.registry = TaskRegistry() # Dicionário de registro das tarefas
        self.queue = TaskQueue() # Fila de execução
        self.workflow = WorkflowService() # Serviço de regras de transição
        self.history = HistoryService() # Pilha de histórico para undo
        self.dependencies = DependencyGraph() # Grafo para detectar ciclos

    def create_task(self, title, priority: TaskPriority, parent_id=None):

        prefix = title[:3].upper()
        task_id = generate_id(prefix=prefix)
        
        # Cria a tarefa com suporte a hierarquia
        task = Task(task_id, title, priority, parent_id=parent_id)
        self.registry.add(task)

        # Se houver um pai, registra a relação na árvore
        if parent_id:
            parent_task = self.registry.get(parent_id)
            if parent_task:
                parent_task.subtasks.append(task)

        def undo():
            if parent_id:
                parent_task = self.registry.get(parent_id)
                if parent_task:
                    parent_task.subtasks.remove(task)
            # Remove a tarefa do registro em caso de desfazer
            del self.registry.tasks[task.id]

        self.history.record(undo)
        return task

    def add_dependency(self, task_id, depends_on_id):
        # Adiciona no grafo de algoritmos para checar ciclos
        self.dependencies.add_dependency(task_id, depends_on_id)

        if self.dependencies.has_cycle():
            raise Exception("Dependência cíclica detectada!")

        # Adiciona a dependência no objeto da tarefa para consulta de status
        task = self.registry.get(task_id)
        if task:
            task.dependencies.add(depends_on_id)

    def start_task(self):
        # Ordena as tarefas por prioridade antes de tentar iniciar
        tasks = sort_by_priority(self.registry.all_tasks())

        for task in tasks:
            if self.workflow.can_start(task, self.registry):
                task.status = TaskStatus.IN_PROGRESS
                self.queue.enqueue(task)

                def undo():
                    task.status = TaskStatus.BACKLOG
                    self.queue.dequeue() 

                self.history.record(undo)
                print(f"Iniciando {task}")
                return
        
        print("Aviso: Nenhuma tarefa disponível para iniciar (bloqueada por dependências, hierarquia ou execução atual).")

    def finish_task(self):
        
        temp_storage = []
        task_to_finish = None

        while not self.queue.is_empty():
            task = self.queue.dequeue()
            if self.workflow.can_finish(task):
                task_to_finish = task
                break
            else:
                temp_storage.append(task)

        # Devolve para a fila os que ainda não podem ser finalizados (mantendo a ordem original)
        for t in temp_storage:
            self.queue.enqueue(t)

        if not task_to_finish:
            print("Não há tarefas em progresso que possam ser finalizadas (verifique se há subtarefas pendentes).")
            return

        # Define como concluído
        task_to_finish.status = TaskStatus.DONE
        print(f"Finalizando {task_to_finish}")

        def undo():
            # Reverte para progresso e reinsere na fila
            task_to_finish.status = TaskStatus.IN_PROGRESS
            self.queue.enqueue(task_to_finish)

        self.history.record(undo)

    def undo_last_action(self):
        self.history.undo()
