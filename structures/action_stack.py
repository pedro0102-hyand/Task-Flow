class ActionStack:

    def __init__(self):

        self.stack = []
    
    def push(self, action):

        self.stack.append(action)
    
    def pop(self):

        if not self.stack:
            return None
        return self.stack.pop()