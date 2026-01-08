class DependencyGraph:

    def __init__(self):

        self.graph = {} # estrutura interna do grafo

    def add_dependency(self, task_id, depends_on_id):

        self.graph.setdefault(task_id, set()).add(depends_on_id)
    
    def has_cycle(self): # detecta ciclos no grafo

        visited = set() # vértices já processados
        stack = set() # vértices no caminho atual

        def dfs(node):

            if node in stack:
                return True # ocorre ciclo
            if node in visited:
                return False
            
            visited.add(node)
            stack.add(node)

            for neighbor in self.graph.get(node, []):
                if dfs(neighbor):
                    return True
            
            stack.remove(node)
            return False
        
        return any(dfs(node) for node in self.graph)