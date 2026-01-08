from core.enums import TaskStatus

class Workflowservice:

    def can_start(self, task):

        return task.status == TaskStatus.BACKLOG
    
    def can_finish(self, task):

        return task.status == TaskStatus.IN_PROGRESS
    
    