from core.enums import TaskStatus

class WorkflowService:

    def can_start(self, task, registry):

        # Verificando se a tarefa está em backlog
        if task.status != TaskStatus.BACKLOG:
            return False
        
        # Verificando se as dependencias estao concluidas
        for dep_id in task.dependencies:

            dep_task = registry.get(dep_id)
            if dep_task is None or dep_task.status != TaskStatus.DONE:
                return False
        
        return True
    
    def can_finish(self, task):

        return task.status == TaskStatus.IN_PROGRESS
    
    