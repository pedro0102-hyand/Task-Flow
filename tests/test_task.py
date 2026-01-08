from services.task_service import TaskService
from core.enums import TaskStatus

def test_complete_task_workflow():
    service = TaskService()

    # Criar múltiplas tarefas
    task_low = service.create_task("Baixa prioridade", 5)
    task_high = service.create_task("Alta prioridade", 1)

    # Estado inicial
    assert task_low.status == TaskStatus.BACKLOG
    assert task_high.status == TaskStatus.BACKLOG

    # Iniciar tarefa (deve pegar a de maior prioridade)
    service.start_task()
    assert task_high.status == TaskStatus.IN_PROGRESS
    assert task_low.status == TaskStatus.BACKLOG

    # Iniciar outra (não deve iniciar, pois já há uma em progresso)
    service.start_task()
    assert task_low.status == TaskStatus.BACKLOG

    # Finalizar tarefa atual
    service.finish_task()
    assert task_high.status == TaskStatus.DONE

    # Undo da finalização
    service.undo_last_action()
    assert task_high.status == TaskStatus.IN_PROGRESS

    # Finalizar novamente
    service.finish_task()
    assert task_high.status == TaskStatus.DONE

    # Agora pode iniciar a próxima
    service.start_task()
    assert task_low.status == TaskStatus.IN_PROGRESS

    # Undo do início da segunda task
    service.undo_last_action()
    assert task_low.status == TaskStatus.BACKLOG
