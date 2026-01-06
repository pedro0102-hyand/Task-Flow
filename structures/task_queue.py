from collections import deque

class TaskQueue:

    def __init__(self):

        self.queue = deque() # fila vazia
    
    def enqueue(self,task): 

        self.queue.append(task) # adicionar no fim da fila
    
    def dequeue(self):

        if not self.queue:
            return None
        return self.queue.popleft() # melhor eficiencia computacional
    
    def is_empty(self):

        return len(self.queue) == 0