# Sistema de Gerenciamento de Tarefas Hierárquico

Um sistema de gerenciamento de tarefas desenvolvido em Python que demonstra a aplicação prática de estruturas de dados e algoritmos fundamentais da ciência da computação.

## 🎯 Objetivo

Este projeto foi desenvolvido com propósito educacional para demonstrar a implementação e integração de:

- Estruturas de dados clássicas (filas, pilhas, grafos, árvores)
- Algoritmos de busca e ordenação
- Padrões de design de software
- Validação de regras de negócio complexas

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas bem definida:

```
├── core/              # Modelos de domínio e enumerações
├── structures/        # Implementações de estruturas de dados
├── algorithms/        # Algoritmos (detecção de ciclos, ordenação)
├── services/          # Lógica de negócio e orquestração
├── utils/             # Utilitários (geração de IDs)
└── tests/             # Testes automatizados
```

## 🚀 Funcionalidades

### 1. Hierarquia de Tarefas
- Criação de tarefas principais e subtarefas
- Validação de dependências hierárquicas
- Subtarefas bloqueiam a finalização da tarefa pai

### 2. Sistema de Prioridades
Quatro níveis de prioridade usando Enums:
- `CRITICAL` (1)
- `HIGH` (2)
- `MEDIUM` (3)
- `LOW` (4)

### 3. Gerenciamento de Dependências
- Grafo direcionado para modelar dependências
- Detecção de ciclos usando DFS
- Validação automática antes de adicionar dependências

### 4. Workflow de Estados
Máquina de estados com três status:
- `BACKLOG` - Tarefa criada, aguardando início
- `IN_PROGRESS` - Tarefa em execução
- `DONE` - Tarefa concluída

### 5. Controle de Concorrência
- Apenas uma árvore de tarefas pode estar em progresso simultaneamente
- Subtarefas podem executar concorrentemente com seus pais

### 6. Histórico e Undo
- Pilha de ações para desfazer operações
- Suporte a undo em criação, início e finalização de tarefas

## 📊 Estruturas de Dados Implementadas

### Fila (Queue)
```python
# structures/task_queue.py
# Gerencia tarefas em execução usando collections.deque
```

### Pilha (Stack)
```python
# structures/action_stack.py
# Armazena ações para funcionalidade de undo
```

### Grafo Direcionado
```python
# algorithms/dependency_graph.py
# Modela dependências e detecta ciclos com DFS
```

### Árvore
```python
# Hierarquia implementada em core/task.py
# Relação pai-filho com lista de subtarefas
```

### Registro (Dictionary)
```python
# structures/task_registry.py
# Armazenamento O(1) para busca de tarefas por ID
```

## 🔧 Instalação e Uso

### Pré-requisitos
- Python 3.7+

### Executando o Projeto

```bash
# Clone o repositório
git clone <seu-repositorio>
cd <nome-do-projeto>

# Execute o exemplo principal
python main.py
```

### Exemplo de Uso

```python
from services.task_service import TaskService
from core.enums import TaskPriority

service = TaskService()

# Criar tarefa principal
pai = service.create_task("Projeto API", priority=TaskPriority.CRITICAL)

# Criar subtarefa
sub = service.create_task(
    "Configurar Banco", 
    priority=TaskPriority.HIGH, 
    parent_id=pai.id
)

# Iniciar tarefas (ordem automática por prioridade)
service.start_task()  # Inicia o pai
service.start_task()  # Inicia a subtarefa

# Finalizar tarefas
service.finish_task()  # Finaliza subtarefa primeiro
service.finish_task()  # Depois o pai

# Desfazer última ação
service.undo_last_action()
```

## 🧪 Executando Testes

```bash
# Executar testes
python -m pytest tests/

# Ou executar teste específico
python tests/test_task.py
```

## 📝 Regras de Negócio

### Início de Tarefa
1. Tarefa deve estar em `BACKLOG`
2. Se for subtarefa, o pai deve estar `IN_PROGRESS`
3. Não pode haver outra árvore de tarefas em execução
4. Todas as dependências devem estar `DONE`

### Finalização de Tarefa
1. Tarefa deve estar em `IN_PROGRESS`
2. Todas as subtarefas devem estar `DONE`

### Dependências
1. Não podem criar ciclos
2. Validação automática ao adicionar dependência

## 🎓 Conceitos Aplicados

- **DFS (Depth-First Search)**: Detecção de ciclos em grafos
- **FIFO (First In, First Out)**: Gerenciamento de fila de tarefas
- **LIFO (Last In, First Out)**: Pilha de histórico
- **Command Pattern**: Implementação de undo
- **State Machine**: Transições de estado validadas
- **Service Layer**: Separação de responsabilidades
- **Type Safety**: Uso de Enums para estados e prioridades

## 🛠️ Tecnologias

- **Python 3.7+**
- **collections.deque**: Implementação eficiente de fila
- **uuid**: Geração de IDs únicos
- **enum**: Type-safe enumerations

## 📈 Complexidade Computacional

| Operação | Complexidade |
|----------|-------------|
| Criar tarefa | O(1) |
| Buscar tarefa | O(1) |
| Iniciar tarefa | O(n log n) - ordenação |
| Finalizar tarefa | O(n) - busca na fila |
| Detectar ciclo | O(V + E) - DFS |
| Undo | O(1) |

