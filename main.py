from services.task_service import TaskService
from core.enums import TaskStatus

def main():
    service = TaskService()

    print("=== 1. Criando tarefas com prioridades ===")
    # t1 tem maior prioridade (1), t2 depende de t1
    t1 = service.create_task("Configurar Banco de Dados", priority=1)
    t2 = service.create_task("Implementar Repositório", priority=2)
    
    print(f"Tarefa 1: {t1.title} (Prioridade: {t1.priority})")
    print(f"Tarefa 2: {t2.title} (Prioridade: {t2.priority})")

    print("\n=== 2. Definindo dependências ===")
    # "Implementar Repositório" depende de "Configurar Banco de Dados"
    service.add_dependency(t2.id, t1.id)
    print(f"Dependência criada: '{t2.title}' depende de '{t1.title}'")

    print("\n=== 3. Testando Validação de Dependência ===")
    # Tentaremos iniciar a próxima tarefa disponível.
    # Mesmo se t2 tivesse prioridade maior, ela não deveria iniciar sem t1 estar DONE.
    service.start_task() 
    print(f"Status '{t1.title}': {t1.status.name}")
    print(f"Status '{t2.title}': {t2.status.name}")

    print("\n=== 4. Tentando iniciar t2 enquanto t1 está IN_PROGRESS ===")
    # t1 está em progresso, mas não concluída. t2 ainda deve ser bloqueada.
    service.start_task()
    print(f"Status '{t2.title}' após tentativa: {t2.status.name} (Deve continuar BACKLOG)")

    print("\n=== 5. Finalizando t1 e liberando t2 ===")
    service.finish_task() # Conclui t1
    print(f"Status '{t1.title}': {t1.status.name}")
    
    service.start_task() # Agora deve iniciar t2
    print(f"Status '{t2.title}' após t1 concluída: {t2.status.name} (Deve ser IN_PROGRESS)")

    print("\n=== 6. Testando Desfazer (Undo) ===")
    service.undo_last_action()
    print(f"Status '{t2.title}' após Undo: {t2.status.name} (Volta para BACKLOG)")

    print("\n=== 7. Estado Final do Registro ===")
    for task in service.registry.all_tasks():
        print(f"ID: {task.id[:8]}... | {task.title} -> {task.status.name}")

if __name__ == "__main__":
    main()
