
# coding: utf-8

# In[6]:

import util
import search
from graphviz import Graph, Digraph
from IPython.display import display


class graph_problem(search.SearchProblem):
    def __init__(self, vertices, edges):
        self.G = {v:{} for v in vertices}
        for v1, v2, c in edges:
            (self.G[v1])[v2] = c
        self.start = vertices[0]
        self.goal = vertices[-1]

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return self.goal == state
    
    def setGoalState(self, state):
        self.goal = state

    def getSuccessors(self, state):
        successors = [(suc, state + '->' + suc,
                       (self.G[state])[suc]) for suc in self.G[state]]
        return successors

    def getDot(self, color):
        dot = Graph(graph_attr = {'size':'3.5'})
        for node in self.G:
            if not node in color:
                dot.node(node)
            else:
                dot.node(node, style = 'filled', color = color[node])
        for n1 in self.G:
            for n2 in self.G[n1]:
                if n1 < n2:
                    dot.edge(n1, n2)
        return dot
    
class search_tree():
    def __init__(self):
        self.graph = Digraph()

    def addEdge(self, source, action, target):
        self.graph.edge(source, target, action)

    def getDot(self):
        return self.graph


def general_ui_search(problem, frontier_class):
    visited = {}
    tree = search_tree()
    state = problem.getStartState()
    visited[state] = 'gray'
#    display(problem.getDot(visited))
    frontier = frontier_class()
    frontier.push((state, []))
    while not frontier.isEmpty():
        u, actions = frontier.pop()
#        print 'Pop:', u
        for v, action, cost in problem.getSuccessors(u):
            if not v in visited:
                tree.addEdge(u, action, v)
                if problem.isGoalState(v):
                    return  actions + [action], tree
                visited[v] = 'gray'
                frontier.push((v, actions + [action]))
#            display(problem.getDot(visited))
#            display(tree.getDot())
        visited[u] = 'green'
    return [], tree


def dfs(problem):
   return general_ui_search(problem, util.Stack)


def bfs(problem):
   return general_ui_search(problem, util.Queue)


# In[7]:

edges1 = [
    ('0/0', '0/5', 1), ('0/0', '2/0', 1), 
    ('0/1', '0/0', 1), ('0/1', '2/1', 1), ('0/1', '0/5', 1), ('0/1', '1/0', 1), 
    ('0/2', '0/0', 1), ('0/2', '2/2', 1), ('0/2', '0/5', 1), ('0/2', '2/0', 1),
    ('0/3', '0/0', 1), ('0/3', '2/3', 1), ('0/3', '0/5', 1), ('0/3', '2/1', 1),
    ('0/4', '0/0', 1), ('0/4', '2/4', 1), ('0/4', '0/5', 1), ('0/4', '2/2', 1),
    ('0/5', '0/0', 1), ('0/5', '2/5', 1), ('0/5', '2/3', 1),
    ('1/0', '0/0', 1), ('1/0', '2/0', 1), ('1/0', '1/5', 1), ('1/0', '0/1', 1),
    ('1/5', '0/5', 1), ('1/5', '1/0', 1), ('1/5', '2/0', 1), ('1/5', '2/4', 1),
    ('2/0', '0/0', 1), ('2/0', '2/5', 1), ('2/0', '0/2', 1),
    ('2/1', '0/1', 1), ('2/1', '2/0', 1), ('2/1', '2/5', 1), ('2/1', '0/3', 1),
    ('2/2', '0/2', 1), ('2/2', '2/0', 1), ('2/2', '2/5', 1), ('2/2', '0/4', 1),
    ('2/3', '0/3', 1), ('2/3', '2/0', 1), ('2/3', '2/5', 1), ('2/3', '0/5', 1),
    ('2/4', '0/4', 1), ('2/4', '2/0', 1), ('2/4', '2/5', 1), ('2/4', '1/5', 1),
    ('2/5', '0/5', 1), ('2/5', '2/0', 1), 
         ]
vertices1 = ['0/0', '0/2', '0/3', '0/4', '0/5', '1/0', '1/5', '2/0', '2/1', '2/2', '2/3', '2/4', '2/5', '0/1']
problem1 = graph_problem(vertices1, edges1)
print problem1.G
print problem1.G['0/0']
dot = problem1.getDot({})
display(dot)


# In[8]:

goal_states = ['0/1', '1/0', '1/5', '2/1']

for state in goal_states:
    print(state)
    problem1.setGoalState(state)
    actions, tree = dfs(problem1)
    print actions
    display(tree.getDot())


# In[10]:

goal_states = ['0/1', '1/0', '1/5', '2/1']

for state in goal_states:
    print(state)
    problem1.setGoalState(state)
    actions, tree = bfs(problem1)
    print actions
    display(tree.getDot())




