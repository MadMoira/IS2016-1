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

