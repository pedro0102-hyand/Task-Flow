from core.task import Task
from core.enums import TaskStatus
from structures.task_queue import TaskQueue
from structures.task_registry import TaskRegistry
from services.workflow_service import WorkflowService
from services.history_service import HistoryService
from algorithms.dependency_graph import DependencyGraph
from algorithms.sorting import sort_by_priority
from utils.id_generator import generate_id

# Define e centraliza as regras do sistema
class TaskService:

    def __init__(self):
        self.registry = TaskRegistry() # Dicionário de registro das tarefas
        self.queue = TaskQueue() # Fila de execução
        self.workflow = WorkflowService() # Serviço de regras de transição
        self.history = HistoryService() # Pilha de histórico para undo
        self.dependencies = DependencyGraph() # Grafo para detectar ciclos

    def create_task(self, title, priority):
        # Melhoria: Gera um ID amigável usando as primeiras 3 letras do título como prefixo
        prefix = title[:3].upper()
        task_id = generate_id(prefix=prefix)
        
        task = Task(task_id, title, priority)
        self.registry.add(task)

        def undo():
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
            # Melhoria: Passa o 'registry' para o workflow validar se dependências estão DONE
            if self.workflow.can_start(task, self.registry):
                task.status = TaskStatus.IN_PROGRESS
                self.queue.enqueue(task)

                def undo():
                    # Reverte o estado e retira a lógica de execução
                    task.status = TaskStatus.BACKLOG
                    # Nota: Em sistemas complexos, removeria especificamente este item da TaskQueue

                self.history.record(undo)
                print(f"Iniciando {task}")
                return
        
        print("Nenhuma tarefa disponível para iniciar (bloqueada por dependências ou sem tarefas no Backlog).")

    def finish_task(self):
        # Remove a tarefa da fila de execução (FIFO)
        task = self.queue.dequeue()

        # Valida se a tarefa pode ser finalizada (deve estar IN_PROGRESS)
        if not task or not self.workflow.can_finish(task):
            print("Não há tarefas em progresso para finalizar.")
            return

        # Define como concluído
        task.status = TaskStatus.DONE

        def undo():
            # Reverte para progresso e reinsere na fila
            task.status = TaskStatus.IN_PROGRESS
            self.queue.enqueue(task)

        self.history.record(undo)
        print(f"Finalizando {task}")

    def undo_last_action(self):
        # Executa a última função de desfazer armazenada no HistoryService
        self.history.undo()
