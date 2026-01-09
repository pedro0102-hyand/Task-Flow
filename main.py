from services.task_service import TaskService
from core.enums import TaskStatus

def main():
    service = TaskService()

    print("=== 1. Criando tarefas com IDs amigáveis ===")
    # As tarefas agora geram IDs baseados no prefixo do título
    t1 = service.create_task("Banco de Dados", priority=1)
    t2 = service.create_task("Repositorio", priority=2)
    t3 = service.create_task("Interface", priority=3)
    
    # Exibe os IDs gerados para verificar o novo formato (ex: BAN-xxxxx)
    print(f"Tarefa 1: {t1.title} | ID: {t1.id} | Prioridade: {t1.priority}")
    print(f"Tarefa 2: {t2.title} | ID: {t2.id} | Prioridade: {t2.priority}")
    print(f"Tarefa 3: {t3.title} | ID: {t3.id} | Prioridade: {t3.priority}")

    print("\n=== 2. Definindo dependências ===")
    # 'Repositorio' depende de 'Banco de Dados'
    service.add_dependency(t2.id, t1.id)
    # 'Interface' depende de 'Repositorio'
    service.add_dependency(t3.id, t2.id)
    print(f"Configurado: {t3.title} -> {t2.title} -> {t1.title}")

    print("\n=== 3. Testando Validação de Dependência (Bloqueio) ===")
    # Tenta iniciar tarefas. Apenas t1 deve iniciar pois t2 e t3 estão bloqueadas
    service.start_task() 
    print(f"Status '{t1.title}': {t1.status.name}")
    print(f"Status '{t2.title}': {t2.status.name} (Deve ser BACKLOG)")

    print("\n=== 4. Tentando iniciar t2 com t1 ainda IN_PROGRESS ===")
    # t2 não deve iniciar enquanto t1 não for DONE
    service.start_task()
    print(f"Status '{t2.title}': {t2.status.name} (Ainda deve ser BACKLOG)")

    print("\n=== 5. Finalizando t1 e liberando t2 ===")
    service.finish_task() # Move t1 para DONE
    print(f"Status '{t1.title}': {t1.status.name}")
    
    service.start_task() # Agora t2 pode iniciar
    print(f"Status '{t2.title}': {t2.status.name} (Agora deve ser IN_PROGRESS)")

    print("\n=== 6. Testando Desfazer (Undo) ===")
    # Desfaz o início da t2, voltando-a para o BACKLOG
    service.undo_last_action()
    print(f"Status '{t2.title}' após Undo: {t2.status.name} (Voltou para BACKLOG)")

    print("\n=== 7. Fluxo Final: Concluindo tudo ===")
    service.start_task()  # Re-inicia t2
    service.finish_task() # Finaliza t2
    service.start_task()  # Inicia t3 (agora que t2 é DONE)
    service.finish_task() # Finaliza t3

    print("\n=== 8. Estado Final do Registro ===")
    for task in service.registry.all_tasks():
        # Exibe o estado final de todas as tarefas
        print(f"ID: {task.id} | {task.title} -> {task.status.name}")

if __name__ == "__main__":
    main()
