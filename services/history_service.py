from structures.action_stack import ActionStack

class HistoryService:

    def __init__(self):

        self.actions = ActionStack()

    def record(self, undo_action):

        self.actions.push(undo_action)
    
    def undo(self):

        action = self.actions.pop()
        if action:
            action()