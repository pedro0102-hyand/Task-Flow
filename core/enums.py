from enum import Enum

class TaskStatus(Enum):

    BACKLOG = "backlog"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskPriority(Enum):

    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

