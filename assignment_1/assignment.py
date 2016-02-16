from search_base import *

edges1 = [('v', 'r', 1), ('r', 's', 1), ('w', 't', 1),('s','w', 1),
         ('w', 'x', 1), ('t', 'x', 1), ('t', 'u', 1), ('x', 'y', 1),
         ('u', 'y', 1)]
vertices1 = ['s', 'r', 't', 'u', 'v', 'w', 'x', 'y']
problem1 = graph_problem(vertices1, edges1)
print problem1.G
print problem1.G['w']
print problem1.getStartState()
print problem1.isGoalState('y')
dot = problem1.getDot({})
display(dot)


# actions, tree = dfs(problem1)
# print actions
# display(tree.getDot())
#
# actions1, tree1 = bfs(problem1)
# print actions
# display(tree1.getDot())