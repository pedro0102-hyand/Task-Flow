from services.task_service import TaskService
from core.enums import TaskStatus, TaskPriority # Importação do TaskPriority adicionada

def main():
    service = TaskService()

    print("=== 1. Criando Hierarquia com Prioridades Enum ===")
    # Agora utilizamos TaskPriority.NOME em vez de números
    pai = service.create_task("Projeto API", priority=TaskPriority.CRITICAL)
    
    # Subtarefa vinculada ao ID do pai com prioridade definida via Enum
    sub1 = service.create_task("Configurar Banco de Dados", priority=TaskPriority.HIGH, parent_id=pai.id)
    
    print(f"Tarefa Principal: {pai.title} | ID: {pai.id} | Prioridade: {pai.priority.name}")
    print(f"  -> Subtarefa: {sub1.title} | ID: {sub1.id} | Prioridade: {sub1.priority.name}")

    print("\n=== 2. Iniciando Fluxo Hierárquico ===")
    # 2.1 Iniciar o Pai (Deve ser o primeiro por ser CRITICAL e não ter dependências)
    service.start_task() 
    print(f"Status Pai: {pai.status.name}")

    # 2.2 Iniciar o Filho (Permitido agora que o pai está IN_PROGRESS)
    service.start_task()
    print(f"Status Filho: {sub1.status.name}")

    print("\n=== 3. Testando Bloqueio de Finalização do Pai ===")
    # Tenta finalizar o Pai. A lógica de busca na fila deve encontrar o filho primeiro,
    # pois o pai não pode ser finalizado enquanto o filho não for DONE.
    service.finish_task() 
    
    print(f"Status Filho após tentativa de finalização: {sub1.status.name} (Deve ser DONE)")
    print(f"Status Pai após tentativa de finalização: {pai.status.name} (Deve continuar IN_PROGRESS)")

    print("\n=== 4. Finalizando o Pai após Filho concluído ===")
    # Com o filho DONE, o pai agora pode ser finalizado com sucesso
    service.finish_task() 
    print(f"Status Pai final: {pai.status.name} (Agora deve ser DONE)")

    print("\n=== 5. Testando Desfazer (Undo) na Árvore ===")
    # Desfaz a última ação (a finalização do Pai)
    service.undo_last_action()
    print(f"Status Pai após Undo: {pai.status.name} (Voltou para IN_PROGRESS)")

    print("\n=== 6. Estado Final do Registro (Visão Geral) ===")
    for task in service.registry.all_tasks():
        # Exibição do status e do nome da prioridade para conferência
        print(f"ID: {task.id} | {task.title} | Prioridade: {task.priority.name} -> {task.status.name}")

if __name__ == "__main__":
    main()
