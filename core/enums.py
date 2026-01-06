from enum import Enum

class TaskStatus(Enum):

    BACKLOG = "backlog"
    IN_PROGRESS = "in_progress"
    DONE = "done"