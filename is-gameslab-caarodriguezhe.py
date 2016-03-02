
# coding: utf-8

# In[1]:

class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement
    legal_moves, make_move, utility, and terminal_test. You may
    override display and successors or you can inherit their default
    methods. You will also need to set the .initial attribute to the
    initial state; this can be done in the constructor."""

    def legal_moves(self, state):
        "Return a list of the allowable moves at this point."
        abstract

    def make_move(self, move, state):
        "Return the state that results from making a move from a state."
        abstract

    def utility(self, state, player):
        "Return the value of this final state to player."
        abstract

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.legal_moves(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        print state

    def successors(self, state):
        "Return a list of legal (move, state) pairs."
        return [(move, self.make_move(move, state))
                for move in self.legal_moves(state)]

    def __repr__(self):
        return '<%s>' % self.__class__.__name__


# In[2]:

def argmin(seq, fn):
    """Return an element with lowest fn(seq[i]) score; tie goes to first one.
    >>> argmin(['one', 'to', 'three'], len)
    'to'
    """
    print("Prueba 5")
    best = seq[0]
    print(best)
    best_score = fn(best)
    print("Prueba 6")
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score
    print("Prueba 7")
    return best


def argmax(seq, fn):
    """Return an element with highest fn(seq[i]) score; tie goes to first one.
    # >>> argmax(['one', 'to', 'three'], len)
    'three'
    """
    return argmin(seq, lambda x: -fn(x))


# In[3]:

def alphabeta_search(state, game, d=float('inf'), cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state, player)
        v = -float('inf')
        for (a, s) in game.successors(state):
            v = max(v, min_value(s, alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        # print("Entro min value")
        # print(state)
        # print(game.terminal_test(state))
        # print(cutoff_test(state, depth))
        if cutoff_test(state, depth):
            # print("algun día sale 1")
            return eval_fn(state, player)
        # print("paso")
        v = float('inf')
        for (a, s) in game.successors(state):
            # print("algun día sale 2")
            v = min(v, max_value(s, alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        # print("algun día sale 3")
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    print("Prueba 1")
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or game.terminal_test(state)))
    print("Prueba 2")
    eval_fn = eval_fn or (lambda state, player: game.utility(state, player))
    print("Prueba 3")
    action, state = argmax(game.successors(state),
                           lambda ((a, s)): min_value(s, -float('inf'), float('inf'), 0))
    print("prueba 4")
    return action





# In[4]:


def num_or_str(x):
    """The argument is a string; convert to a number if possible, or strip it.
    >>> num_or_str('42')
    42
    >>> num_or_str(' 42x ')
    '42x'
    """
    if isnumber(x): return x
    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
                return str(x).strip()

def isnumber(x):
    "Is x a number? We say it is if it has a __int__ method."
    return hasattr(x, '__int__')


# In[5]:

def query_player(game, state):
    "Make a move by querying standard input."
    game.display(state)
    return num_or_str(raw_input('Your move? '))


# In[6]:

import random

def random_player(game, state):
    "A player that chooses a legal move at random."
    return random.choice(game.legal_moves(state))


# In[7]:

def alphabeta_player(game, state):
    return alphabeta_search(state, game)


# In[18]:

def play_game(game, *players):
    "Play an n-person, move-alternating game."
    state = game.initial
    while True:
        for player in players:
            print player
            move = player(game, state)
            state = game.make_move(move, state)
            if game.terminal_test(state):
                return game.utility(state, 0)


# In[9]:

class Struct:
    """Create an instance with argument=value slots.
    This is for making a lightweight object whose class doesn't matter."""
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __cmp__(self, other):
        if isinstance(other, Struct):
            return cmp(self.__dict__, other.__dict__)
        else:
            return cmp(self.__dict__, other)

    def __repr__(self):
        args = ['%s=%s' % (k, repr(v)) for (k, v) in vars(self).items()]
        return 'Struct(%s)' % ', '.join(args)

    def __getitem__(self, value):
        return self.__dict__.get(value)


# In[10]:

class LastStone(Game):
    def __init__(self, stones):
        self.initial = Struct(to_move=0, heap = stones)

    def legal_moves(self, state):
        "Return a list of the allowable moves at this point."
        return range(1, min(3, state.heap) + 1)

    def make_move(self, move, state):
        "Return the state that results from making a move from a state."
        return Struct(to_move = 1 - state.to_move,
                      heap = state.heap - move)

    def utility(self, state, player):
        "Return the value of this final state to player."
        if state.to_move == player:
            return -1
        else:
            return 1

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.legal_moves(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        print state

    def successors(self, state):
        "Return a list of legal (move, state) pairs."
#         print([(move, self.make_move(move, state))
#                 for move in self.legal_moves(state)])
        return [(move, self.make_move(move, state))
                for move in self.legal_moves(state)]


# In[11]:

# play_game(LastStone(17), query_player, alphabeta_player)


# In[12]:

def eval_fn(state, player):

    if state.heap % 4 == 0:
        if state.to_move == player:
            return -1
        else:
            return 1
    else:
        if state.to_move == player:
            return 1
        else:
            return -1


def smart_player(game, state):
    return alphabeta_search(state, game, d=2, eval_fn=eval_fn)


# result = play_game(LastStone(12), smart_player, alphabeta_player)
# if result == 1:
#     print "Smart player wins"
# else:
#     print "Smart player loses"


# In[13]:

class LastStone3Heaps(Game):
    def __init__(self, k, heap1, heap2, heap3):
        self.initial = Struct(to_move=0, heap1=heap1, heap2=heap2, heap3=heap3)
        self.max_stones = k
        self.expanded_states = 0

    def legal_moves(self, state):
        "Return a list of the allowable moves at this point."
        heaps = ['heap1', 'heap2', 'heap3']
        valid_moves = []
        for heap in heaps:
            valid_moves += [(heap, move)
                            for move in range(1, min(self.max_stones, state[heap]) + 1)]
        return valid_moves

    def make_move(self, move, state):
        "Return the state that results from making a move from a state."
        heap1 = state['heap1']
        heap2 = state['heap2']
        heap3 = state['heap3']
        if move[0] == 'heap1':
            heap1 -= move[1]
        elif move[0] == 'heap2':
            heap2 -= move[1]
        elif move[0] == 'heap3':
            heap3 -= move[1]
        return Struct(to_move = 1 - state.to_move,
                      heap1=heap1,
                      heap2=heap2,
                      heap3=heap3)

    def utility(self, state, player):
        "Return the value of this final state to player."
        if state.to_move == player:
            return -1
        else:
            return 1

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.legal_moves(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        return state

    def successors(self, state):
        "Return a list of legal (move, state) pairs."
        successors = [(move, self.make_move(move, state))
                for move in self.legal_moves(state)]
        self.expanded_states += len(successors)
        return successors


# In[16]:

test_state = Struct(to_move=0, heap1=4, heap2=4, heap3=4)
terminal_state = Struct(to_move=0, heap1=1, heap2=0, heap3=0)
game = LastStone3Heaps(3, 6, 6, 6)
# print game.legal_moves(test_state)
# print game.make_move(('heap1',3), test_state)
# print game.terminal_test(terminal_state)
# print game.successors(test_state)

# In[20]:


def eval_fn(state, player):
    return 0

result = play_game(game, smart_player, alphabeta_player)
print(result)
print(game.expanded_states)


# In[ ]:



