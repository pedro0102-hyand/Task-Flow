from services.task_service import TaskService
from core.enums import TaskStatus

def main():
    service = TaskService()

    print("=== Criando tarefas ===")
    t1 = service.create_task("Criar API", priority=1)
    t2 = service.create_task("Escrever testes", priority=2)
    t3 = service.create_task("Configurar CI", priority=3)

    print(t1)
    print(t2)
    print(t3)

    print("\n=== Definindo dependências ===")
    service.add_dependency(t2.id, t1.id)  # testes dependem da API
    service.add_dependency(t3.id, t2.id)  # CI depende dos testes

    print("\n=== Iniciando fluxo de trabalho ===")
    service.start_task()   # Deve iniciar "Criar API"
    print(f"Status API: {t1.status}")

    service.finish_task()  # Finaliza "Criar API"
    print(f"Status API após finalizar: {t1.status}")

    print("\n=== Iniciando próxima tarefa ===")
    service.start_task()   # Deve iniciar "Escrever testes"
    print(f"Status Testes: {t2.status}")

    print("\n=== Desfazendo última ação (undo) ===")
    service.undo_last_action()
    print(f"Status Testes após undo: {t2.status}")

    print("\n=== Reiniciando tarefa corretamente ===")
    service.start_task()
    service.finish_task()

    print("\n=== Estado final das tarefas ===")
    for task in service.registry.all_tasks():
        print(f"{task.title} -> {task.status}")

if __name__ == "__main__":
    main()
