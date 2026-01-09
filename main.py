from services.task_service import TaskService
from core.enums import TaskStatus

def main():
    service = TaskService()

    print("=== 1. Criando tarefas com IDs amigáveis ===")
    t1 = service.create_task("Banco de Dados", priority=1)
    t2 = service.create_task("Repositorio", priority=2)
    
    print(f"Tarefa 1: {t1.title} | ID: {t1.id}")
    print(f"Tarefa 2: {t2.title} | ID: {t2.id}")

    print("\n=== 2. Definindo dependências ===")
    # Repositorio depende de Banco de Dados
    service.add_dependency(t2.id, t1.id)
    print(f"Configurado: {t2.title} depende de {t1.title}")

    print("\n=== 3. Testando Concorrência e Bloqueio ===")
    # Inicia a primeira tarefa
    service.start_task() 
    print(f"Status '{t1.title}': {t1.status.name}")

    # Tenta iniciar outra tarefa com a primeira ainda em progresso
    print("\n--- Tentativa de iniciar segunda tarefa (deve ser bloqueada) ---")
    service.start_task() 
    print(f"Status '{t2.title}': {t2.status.name} (Deve continuar BACKLOG)")

    print("\n=== 4. Finalizando tarefa atual e liberando a próxima ===")
    service.finish_task() # Finaliza t1
    print(f"Status '{t1.title}': {t1.status.name}")
    
    # Agora sim t2 deve conseguir iniciar
    service.start_task() 
    print(f"Status '{t2.title}': {t2.status.name} (Agora deve ser IN_PROGRESS)")

    print("\n=== 5. Testando Undo da Concorrência ===")
    # Desfaz o início da t2
    service.undo_last_action()
    print(f"Status '{t2.title}' após Undo: {t2.status.name} (Voltou para BACKLOG)")
    
    # Tenta iniciar novamente para garantir que a fila limpou corretamente no undo
    service.start_task()
    print(f"Status '{t2.title}' após reiniciar: {t2.status.name}")

    print("\n=== 6. Estado Final das Tarefas ===")
    for task in service.registry.all_tasks():
        print(f"ID: {task.id} | {task.title} -> {task.status.name}")

if __name__ == "__main__":
    main()
