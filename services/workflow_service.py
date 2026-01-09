from core.enums import TaskStatus

class WorkflowService:

    def can_start(self, task, registry):
        # A tarefa deve estar obrigatoriamente no BACKLOG para iniciar
        if task.status != TaskStatus.BACKLOG:
            return False
        
        # Regra de Árvore: Uma subtarefa só pode iniciar se o seu Pai estiver IN_PROGRESS
        if task.parent_id:
            parent = registry.get(task.parent_id)
            if not parent or parent.status != TaskStatus.IN_PROGRESS:
                return False
        
        # Gestão de Concorrência: Apenas uma "árvore" ou tarefa independente por vez
        for t in registry.all_tasks():
            if t.status == TaskStatus.IN_PROGRESS:
                # Se a tarefa já em progresso for o Pai desta, permitimos a concorrência
                if task.parent_id == t.id:
                    continue
                # Se houver qualquer outra tarefa IN_PROGRESS que não seja o Pai, bloqueia
                return False

        # Verificação de Dependências: Todas as dependências externas devem estar DONE
        for dep_id in task.dependencies:
            dep_task = registry.get(dep_id)
            if dep_task is None or dep_task.status != TaskStatus.DONE:
                return False
        
        return True
    
    def can_finish(self, task):

        if task.status != TaskStatus.IN_PROGRESS:
            return False
            
        for subtask in task.subtasks:
            if subtask.status != TaskStatus.DONE:
                return False
                
        return True
    
    