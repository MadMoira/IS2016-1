
# coding: utf-8

# # Intelligent Systems Assignment 1
#
# ## Masterball solver
#
# **Name:**
#
# **ID:**
#

# ### 1. Create a class to model the Masterball problem

# A Masterball must be represented as an array of arrays with integer values representing the color of the tile in each position:
#
# A solved masterball must look like this:
#
# ```python
# [ [0, 1, 2, 3, 4, 5, 6, 7],
#   [0, 1, 2, 3, 4, 5, 6, 7],
#   [0, 1, 2, 3, 4, 5, 6, 7],
#   [0, 1, 2, 3, 4, 5, 6, 7]
# ]
# ```

# #### Variables modeling the actions

# In[1]:

import time

'''
This variables MUST not be changed.
They represent the movements of the masterball.
'''
R_0 = "Right 0"
R_1 = "Right 1"
R_2 = "Right 2"
R_3 = "Right 3"

V_0 = "Vertical 0"
V_1 = "Vertical 1"
V_2 = "Vertical 2"
V_3 = "Vertical 3"
V_4 = "Vertical 4"
V_5 = "Vertical 5"
V_6 = "Vertical 6"
V_7 = "Vertical 7"


# `R_i` moves the `i`th row to the right. For instance, `R_2` applied to the solved state will produce:
#
# ```python
# [ [0, 1, 2, 3, 4, 5, 6, 7],
#   [0, 1, 2, 3, 4, 5, 6, 7],
#   [7, 0, 1, 2, 3, 4, 5, 6],
#   [0, 1, 2, 3, 4, 5, 6, 7]
# ]
# ```
#
# `V_i` performs a clockwise vertical move starting with the `i`th column
#
# `V_1` applied to the above state will produce:
#
# ```python
# [ [0, 4, 3, 2, 1, 5, 6, 7],
#   [0, 3, 2, 1, 0, 5, 6, 7],
#   [7, 4, 3, 2, 1, 4, 5, 6],
#   [0, 4, 3, 2, 1, 5, 6, 7]
# ]
# ```

# #### The Masterball problem class

# In[90]:

from collections import deque
import search
import copy


class MasterballProblem(search.SearchProblem):

    def __init__(self, startState):
        '''
        Store the initial state in the problem representation and any useful
        data.
        Here are some examples of initial states:
        [[0, 1, 4, 5, 6, 2, 3, 7], [0, 1, 3, 4, 5, 6, 3, 7], [1, 2, 4, 5, 6, 2, 7, 0], [0, 1, 4, 5, 6, 2, 3, 7]]
        [[0, 7, 4, 5, 1, 6, 2, 3], [0, 7, 4, 5, 0, 5, 2, 3], [7, 6, 3, 4, 1, 6, 1, 2], [0, 7, 4, 5, 1, 6, 2, 3]]
        [[0, 1, 6, 4, 5, 2, 3, 7], [0, 2, 6, 5, 1, 3, 4, 7], [0, 2, 6, 5, 1, 3, 4, 7], [0, 5, 6, 4, 1, 2, 3, 7]]
        '''
        self.initial = startState
        self.expanded = 0

    def isGoalState(self, state):
        '''
        Define when a given state is a goal state (A correctly colored masterball)
        '''
        for index in xrange(0,8):
            if not (state[0][index] == state[1][index] == state[2][index] == state[3][index]):
                return False
        return True

    def getStartState(self):
        '''
        Implement a method that returns the start state according to the SearchProblem
        contract.
        '''
        return self.initial

    def getSuccessors(self, state):
        '''
        Implement a successor function: Given a state from the masterball
        return a list of the successors and their corresponding actions.

        This method *must* return a list where each element is a tuple of
        three elements with the state of the masterball in the first position,
        the action (according to the definition above) in the second position,
        and the cost of the action in the last position.

        Note that you should not modify the state.
        '''
        actions = [R_0, R_1, R_2, R_3, V_0, V_1, V_2, V_3, V_4, V_5, V_6, V_7]

        successors = []

        for action in actions:
            movement, column = action.split(' ')

            new_state = copy.deepcopy(state)
            if movement == 'Right':
                moving_row = new_state[int(column)]
                moving_row_deque = deque(moving_row)
                moving_row_deque.rotate(1)
                moving_row = list(moving_row_deque)

                new_state[int(column)] = moving_row

            if movement == 'Vertical':

                if int(column) <= 3:
                    ith = int(column)
                    ith4 = int(column) + 4
                else:
                    ith = int(column)
                    ith4 = int(column) - 4

                temp_ith = []
                temp_ith4 = []

                for index in xrange(0,4):
                    temp_ith.append(new_state[index][ith])
                    temp_ith4.append(new_state[index][ith4])

                temp_ith_deque = deque(temp_ith)
                temp_ith4_deque = deque(temp_ith4)
                temp_ith_deque.rotate(-1)
                temp_ith4_deque.rotate(-1)
                temp_ith = list(temp_ith_deque)
                temp_ith4 = list(temp_ith4_deque)

                for index in xrange(0,4):
                    new_state[index][ith] = temp_ith4[index]
                    new_state[index][ith4] = temp_ith[index]

            successors.append((new_state, (state, action, new_state), 1))

        self.expanded += 1

        return successors


# In[92]:

test_state_0 = [[0, 1, 4, 5, 6, 2, 3, 7],
                [0, 1, 4, 5, 6, 2, 3, 7],
                [1, 4, 5, 6, 2, 3, 7, 0],
                [0, 1, 4, 5, 6, 2, 3, 7]]

test_state_1 = [[0, 1, 4, 5, 6, 2, 3, 7],
                [0, 1, 3, 4, 5, 6, 3, 7],
                [1, 2, 4, 5, 6, 2, 7, 0],
                [0, 1, 4, 5, 6, 2, 3, 7]]

test_state_2 = [[0, 1, 2, 3, 4, 5, 6, 7],
                [0, 1, 2, 3, 4, 5, 6, 7],
                [7, 0, 1, 2, 3, 4, 5, 6],
                [0, 1, 2, 3, 4, 5, 6, 7]]

test_state_3 = [[0, 1, 2, 3, 4, 5, 6, 7],
                [0, 1, 2, 3, 4, 5, 6, 7],
                [0, 1, 2, 3, 4, 5, 6, 7],
                [0, 1, 2, 3, 4, 5, 6, 7]]

test_state_4 = [[4, 1, 2, 0, 3, 5, 6, 7],
                [4, 1, 2, 0, 3, 5, 6, 7],
                [4, 1, 2, 0, 3, 5, 6, 7],
                [4, 1, 2, 0, 3, 5, 6, 7]]

print(test_state_1)
problem = MasterballProblem(test_state_1)

# for successor in successors:
#     print(successor[0])
#     print(successor[1])
#     print(successor[2])
#     print("\n")


# ### 2. Implement iterative deepening search
#
# Follow the example code provided in class and implement iterative deepening search (IDS).

# In[2]:


from search_base import search_tree
from util import Stack


def getStringState(state):

    stringed = ''

    for row in state:
        for element in row:
            stringed += str(element)

    return stringed


def DepthLimitedSearch(problem, depth):
    visited = {}
    tree = search_tree()
    state = problem.getStartState()
    visited[getStringState(state)] = 'gray'
    frontier = Stack()
    frontier.push((state, [], 0))
    while not frontier.isEmpty():
        u, actions, current_depth = frontier.pop()
        for v, action, cost in problem.getSuccessors(u):
            mini_action = action[1]
            stringed_state = getStringState(v)
            if current_depth > depth:
                break
            if not getStringState(v) in visited:
                tree.addEdge(getStringState(u), action[1], getStringState(v))
                if problem.isGoalState(v):
                    return actions + [action[1]], tree
                visited[getStringState(v)] = 'gray'
                frontier.push((v, actions + [action[1]], current_depth+1))
        visited[getStringState(u)] = 'green'
    return [], tree


import sys


def IterativeDeepeningSearch(problem):

    for i in xrange(sys.maxint):
        start_time = time.time()
        actions, tree = DepthLimitedSearch(problem, i)
        print("Para profundidad " + str(i) + " el tiempo fue: " + str(time.time() - start_time))
        if len(actions) > 0:
            return actions, tree, i


actions, tree, depth = IterativeDeepeningSearch(problem)

print("actions")
print(actions)
print(depth)

# def aStarSearch(problem, heuristic):
#     return []
#
#
# # Evaluate it to see what is the maximum depth that it could explore in a reasonable time. Report the results.
#
# # ### 3. Implement different heuristics for the problem
#
# # Implement at least two admissible and consistent heuristics. Compare A* using the heuristics against IDS calculating the number of expanded nodes and the effective branching factor, in the same way as it is done in figure 3.29 of [Russell10].
#
# # In[5]:
#
# def myHeuristic(state):
#     return 0
#
#
# # In[6]:
#
# def solveMasterBall(problem, search_function):
#     '''
#     This function receives a Masterball problem instance and a
#     search_function (IDS or A*S) and must return a list of actions that solve the problem.
#     '''
#     return []
#
#
# problem = MasterballProblem([ [0, 4, 3, 2, 1, 5, 6, 7],
#                               [0, 3, 2, 1, 0, 5, 6, 7],
#                               [7, 4, 3, 2, 1, 4, 5, 6],
#                               [0, 4, 3, 2, 1, 5, 6, 7]])
#
# print solveMasterBall(problem, iterativeDeepeningSearch(problem))
# print solveMasterBall(problem, aStarSearch(problem, myHeuristic))
#
#
# # In[ ]:
