
# coding: utf-8

# In[47]:

import util
import search
from graphviz import Graph, Digraph
from IPython.display import display


class graph_problem(search.SearchProblem):
    def __init__(self, initial_state, first_capacity, second_capacity, required_value):
        self.start = initial_state
        self.first_capacity = first_capacity
        self.second_capacity = second_capacity
        self.required_value = required_value
        
        states, _ = self.getSuccessorStates(self.start)
        
        self.G = {
            self.start: {},
        }
        
        for state in states:
            self.G[self.start][state] = 1
        
    def getSuccessorStates(self, state):
        
        first_jar_value = int(state[0])
        second_jar_value = int(state[2])
        
        # Empty first jar
        temp_first_value = 0
        temp_second_value = second_jar_value
        successor_state_1 = str(temp_first_value)+'/'+str(temp_second_value)
        operation_1 = 'e1'
        
        # Empty second jar
        temp_first_value = first_jar_value
        temp_second_value = 0
        successor_state_2 = str(temp_first_value)+'/'+str(temp_second_value)
        operation_2 = 'e2'
        
        # Fill first jar
        temp_first_value = self.first_capacity
        temp_second_value = second_jar_value
        successor_state_3 = str(temp_first_value)+'/'+str(temp_second_value)
        operation_3 = 'f1'
        
        # Fill second jar
        temp_first_value = first_jar_value
        temp_second_value = self.second_capacity
        successor_state_4 = str(temp_first_value)+'/'+str(temp_second_value)
        operation_4 = 'f2'
        
        # Fill first jar with second jar
        if first_jar_value + second_jar_value >= self.first_capacity:
            temp_first_value = self.first_capacity
            temp_second_value = second_jar_value - self.first_capacity + first_jar_value
        else:
            temp_first_value = second_jar_value + first_jar_value
            temp_second_value = 0
        successor_state_5 = str(temp_first_value)+'/'+str(temp_second_value)
        operation_5 = '2t1'
        
        # Fill second jar with first jar
        if first_jar_value + second_jar_value >= self.second_capacity:
            temp_first_value = second_jar_value - self.second_capacity + first_jar_value
            temp_second_value = self.second_capacity
        else:
            temp_first_value = 0
            temp_second_value = second_jar_value + first_jar_value
        successor_state_6 = str(temp_first_value)+'/'+str(temp_second_value)
        operation_6 = '1t2'
        
        states = [
            successor_state_1,
            successor_state_2,
            successor_state_3,
            successor_state_4,
            successor_state_5,
            successor_state_6,
        ]
        
        operations = [
            operation_1,
            operation_2,
            operation_3,
            operation_4,
            operation_5,
            operation_6,
        ]
        
        return states, operations

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        
        first_jar_value = int(state[0])
        second_jar_value = int(state[2])
        
        if first_jar_value == self.required_value or second_jar_value == self.required_value:
            return True
        return False

    def getSuccessors(self, state):
        
        states, operations = self.getSuccessorStates(state)
        
        successors = []
        
        for index in xrange(0,len(states)):
            if states[index] != state:
                successors.append(
                    (states[index], state+' '+operations[index]+' '+states[index], 1)
                )
        
        #successors = [(suc, state + '->' + suc,
        #               (self.G[state])[suc]) for suc in self.G[state]]
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


# In[48]:

problem1 = graph_problem('0/0', 2, 5, 1)
print problem1.G
print problem1.getSuccessors('0/0')
print problem1.isGoalState('0/0')
print problem1.isGoalState('1/0')
print problem1.isGoalState('0/1')
print problem1.isGoalState('2/5')
#dot = problem1.getDot({})
#display(dot)


# In[49]:

actions, tree = dfs(problem1)
print actions
display(tree.getDot())


# In[50]:

actions, tree = bfs(problem1)
print actions
display(tree.getDot())


# In[ ]:



