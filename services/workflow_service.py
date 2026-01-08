from core.enums import TaskStatus

class WorkflowService:

    def can_start(self, task):

        return task.status == TaskStatus.BACKLOG
    
    def can_finish(self, task):

        return task.status == TaskStatus.IN_PROGRESS
    
    