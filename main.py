from services.task_service import TaskService
from core.enums import TaskStatus

def main():
    service = TaskService()

    print("=== 1. Criando Hierarquia (Pai e Filhos) ===")
    # Criamos uma tarefa principal (Pai)
    pai = service.create_task("Projeto API", priority=1)
    
    # Criamos uma subtarefa vinculada ao ID do pai
    sub1 = service.create_task("Configurar Banco de Dados", priority=1, parent_id=pai.id)
    
    print(f"Tarefa Principal: {pai.title} | ID: {pai.id}")
    print(f"  -> Subtarefa: {sub1.title} | ID: {sub1.id} (Pai: {sub1.parent_id})")

    print("\n=== 2. Iniciando Fluxo Hierárquico ===")
    # 2.1 Iniciar o Pai (Obrigatório antes do filho)
    service.start_task() 
    print(f"Status Pai: {pai.status.name}")

    # 2.2 Iniciar o Filho (Permitido agora que o pai está IN_PROGRESS)
    service.start_task()
    print(f"Status Filho: {sub1.status.name}")

    print("\n=== 3. Testando Bloqueio de Finalização do Pai ===")
    # Tentamos finalizar o Pai. O sistema deve pular o pai na fila e 
    # tentar finalizar o filho, pois o pai depende da conclusão dos filhos.
    service.finish_task() 
    
    print(f"Status Filho após tentativa de finalização: {sub1.status.name} (Deve ser DONE)")
    print(f"Status Pai após tentativa de finalização: {pai.status.name} (Deve continuar IN_PROGRESS)")

    print("\n=== 4. Finalizando o Pai após Filho concluído ===")
    # Agora que o filho está DONE, o pai pode ser finalizado
    service.finish_task() 
    print(f"Status Pai final: {pai.status.name} (Agora deve ser DONE)")

    print("\n=== 5. Testando Desfazer (Undo) na Árvore ===")
    # Desfaz a última ação (Finalização do Pai)
    service.undo_last_action()
    print(f"Status Pai após Undo: {pai.status.name} (Voltou para IN_PROGRESS)")

    print("\n=== 6. Estado Final do Registro (Visão Geral) ===")
    for task in service.registry.all_tasks():
        print(f"ID: {task.id} | {task.title} -> {task.status.name}")

if __name__ == "__main__":
    main()
