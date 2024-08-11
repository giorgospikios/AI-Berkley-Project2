# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """
     
    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """

        # # Collect legal moves and successor states
        # legalMoves = gameState.getLegalActions(0)
        # print(" legalMoves = ", legalMoves)

        # # Choose one of the best actions
        # # scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        # scores = []
        # for action in legalMoves:
        #     print(" gameState = ", gameState)
        #     scores.append(self.evaluationFunction(gameState, action))
        #     print(" self.evaluationFunction(gameState, action) = ", self.evaluationFunction(gameState, action))
        # print(" scores = ", scores)
        # bestScore = max(scores)
        # bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # print(" bestIndices= ", bestIndices)
        # chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        # "Add more of your code here if you want to"

        # print(" legalMoves[chosenIndex] = ", legalMoves[chosenIndex])
        # return legalMoves[chosenIndex]
    

        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successor_gamestate = currentGameState.generatePacmanSuccessor(action)
        new_pos = successor_gamestate.getPacmanPosition()

        current_food = currentGameState.getFood()
        ghost_positions = successor_gamestate.getGhostPositions()
        for ghost_position in ghost_positions:
            
            new_pos_x_coord = new_pos[0] #αποφευγω να παω στη καινουργια θεση αν εκει υπαρχει φανατσμα η΄ακριβως στη διπλανη 
            new_pos_y_coord = new_pos[1]
            ghost_distance_frompacman = util.manhattanDistance(new_pos, ghost_position)
            if (ghost_position == new_pos or ghost_distance_frompacman == 1):
                return float('-inf')
            elif (ghost_position != new_pos or ghost_distance_frompacman != 1) and (current_food[new_pos_x_coord][new_pos_y_coord]): 
                return float('inf') #αν δεν υπαρχει φαντασμα στην καινουργια θεση και στην ακριβως διπλανη αλλα υπαρχει φαγητο τη προτιμαω
        

        min_distance = float('inf') #αν ο pacman δεν απυλειται απο φαντασμα στη καινουργια θεση αλλα δεν υπαρχει και φαγητο βρισκω το κοντινοτερτο φαγητο
        current_food = currentGameState.getFood()
        current_food_list = current_food.asList()
        for food in current_food_list:
            newpos_to_food_dist = util.manhattanDistance(new_pos, food)
            if newpos_to_food_dist < min_distance:
                min_distance = newpos_to_food_dist
        
        return successor_gamestate.getScore() - min_distance

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
    
        def MiniMax(gameState, agent_identifier, depth):

            if gameState.isWin() or gameState.isLose() or depth == self.depth: #base case 
                return self.evaluationFunction(gameState),''
            
            if agent_identifier == 0: #ελεγχω αν ο πρακτορας ειναι ο πακμαν
                max_value = float('-inf')
                legal_actions = gameState.getLegalActions(agent_identifier)
                best_legal_action = ''

                for legal_action in legal_actions:
                    legal_action_tonextstate = gameState.generateSuccessor(agent_identifier, legal_action)
                    minimax_return = MiniMax(legal_action_tonextstate, agent_identifier+1, depth) #καλω αναδρομικα τη MiniMax και προσθετω 1 για να αλλαξω πρακτορα

                    if minimax_return[0] > max_value: #ελεγχω και αντικαθιστω τη μεγιστη τιμη που εχει επιστρεψει καθε αναδρομη 
                        max_value = minimax_return[0]
                        best_legal_action = legal_action

                return max_value, best_legal_action
            
            else:# αν ο πρακτορας δεν ειναι ο pacman ειναι φαντασμα
                min_value = float('inf')
                number_of_agents = gameState.getNumAgents()
                legal_actions = gameState.getLegalActions(agent_identifier)
                best_legal_action = ''

                for legal_action in legal_actions:
                    legal_action_tonextstate = gameState.generateSuccessor(agent_identifier, legal_action)
                    if agent_identifier == number_of_agents-1: #επειδη το βαθος ειναι δυο μετα απο μια αναδρομικη κληση της MiniMax θα αλλαξει ο πρακτορας και θα ξαναγινει ο pacman
                        minimax_return = MiniMax(legal_action_tonextstate, self.index, depth+1)
                    else: 
                        minimax_return = MiniMax(legal_action_tonextstate, agent_identifier+1, depth) #βαθος 2 αρα ξαναλλαζει
                    
                    if minimax_return[0] < min_value: #ελεγχω και αντικαθιστω την ελαχιστη τιμη που εχει επιστρεψει καθε αναδρομη 
                        min_value = minimax_return[0]
                        best_legal_action = legal_action

                return min_value, best_legal_action

        pacmans_best_move = MiniMax(gameState, self.index, 0)
        return pacmans_best_move[1]

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def AlphaBeta(gameState, agent_identifier, depth, a, b):

            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState),''
            
            if agent_identifier == 0:
                max_value = float('-inf')
                legal_actions = gameState.getLegalActions(agent_identifier)
                best_legal_action = ''

                for legal_action in legal_actions:
                    legal_action_tonextstate = gameState.generateSuccessor(agent_identifier, legal_action)
                    minimax_return = AlphaBeta(legal_action_tonextstate, agent_identifier+1, depth, a, b)

                    if minimax_return[0] > max_value:
                        max_value = minimax_return[0]
                        best_legal_action = legal_action

                    if max_value > b: #σε αυτο το σημειο γινεται κλαδεμα αν η μεγιστη τιμη ειναι μεγαλυτερη απο τη b 
                        break

                    if max_value > a:
                        a = max_value

                return max_value, best_legal_action
            
            else:
                min_value = float('inf')
                number_of_agents = gameState.getNumAgents()
                legal_actions = gameState.getLegalActions(agent_identifier)
                best_legal_action = ''

                for legal_action in legal_actions:
                    legal_action_tonextstate = gameState.generateSuccessor(agent_identifier, legal_action)
                    if agent_identifier == number_of_agents-1:
                        minimax_return = AlphaBeta(legal_action_tonextstate, self.index, depth+1, a, b)
                    else: 
                        minimax_return = AlphaBeta(legal_action_tonextstate, agent_identifier+1, depth, a, b)
                    
                    if minimax_return[0] < min_value:
                        min_value = minimax_return[0]
                        best_legal_action = legal_action

                    if min_value < a:
                        break

                    if min_value < b:
                        b = min_value

                return min_value, best_legal_action

        pacmans_best_move = AlphaBeta(gameState, self.index, 0, float('-inf'), float('inf'))
        return pacmans_best_move[1]
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def ExpectiMax(gameState, agent_identifier, depth):

            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState),''
            
            if agent_identifier == 0:
                max_value = float('-inf')
                legal_actions = gameState.getLegalActions(agent_identifier)
                best_legal_action = ''

                for legal_action in legal_actions:
                    legal_action_tonextstate = gameState.generateSuccessor(agent_identifier, legal_action)
                    minimax_return = ExpectiMax(legal_action_tonextstate, agent_identifier+1, depth)

                    if minimax_return[0] > max_value:
                        max_value = minimax_return[0]
                        best_legal_action = legal_action

                return max_value, best_legal_action
            
            else:
                #η λογικη στην expectimax συναρτηση ειναι η ιδια με τη MiniMax με τη διαφορα οτι αντι να βρισκουμαι την ελαχιση πιθανη τιμη καθε φορα που παιζει 
                #ενα φαντασμα υπολογιζουμαι τι πιθανοτητα υπαρχει να κανει μια κινηση 
                number_of_agents = gameState.getNumAgents()
                number_of_actions = len(gameState.getLegalActions(agent_identifier))
                legal_actions = gameState.getLegalActions(agent_identifier)
                chance_node_value = 0

                for legal_action in legal_actions:

                    legal_action_tonextstate = gameState.generateSuccessor(agent_identifier, legal_action)
                    if agent_identifier == number_of_agents-1:
                        expectimax_return = ExpectiMax(legal_action_tonextstate, self.index, depth+1)
                    else: 
                        expectimax_return = ExpectiMax(legal_action_tonextstate, agent_identifier+1, depth)

                    chance_node_value += ((1 / number_of_actions) * expectimax_return[0])
                
                return chance_node_value, ''

        pacmans_best_move = ExpectiMax(gameState, self.index, 0)
        return pacmans_best_move[1]
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #τρεχει μονο τα πρωτα 2 και μετα σταματαει την εστειλα απλα για τη προσπαθεια
    
    food_list = currentGameState.getFood().asList()
    totalCapsules = len(currentGameState.getCapsules())
    totalFood = len(food_list) 
    better_evalfunc = 0 

    
    scared_ghosts = [] #βρισκω ολες τις καταστασεις των φαντασματων 
    attack_ghosts = []
    current_ghosts_state = currentGameState.getGhostStates()
    for ghost in current_ghosts_state:
        is_ghost_scared = ghost.scaredTimer
        if is_ghost_scared:
            scared_ghosts.append(ghost)
        else:
            attack_ghosts.append(ghost)

    better_evalfunc += 1.5 * currentGameState.getScore()

    better_evalfunc += -10 * totalFood

    better_evalfunc += -20 * totalCapsules

    foodots_pacman_distance = []
    pacman_position = currentGameState.getPacmanPosition()
    for food in food_list:
        food_pacman_distance = util.manhattanDistance(pacman_position, food)
        foodots_pacman_distance.append(food_pacman_distance)

    for food in foodots_pacman_distance:
        if food < 3: 
            better_evalfunc += -1 * food
        if food < 7: 
            better_evalfunc += -0.5 * food
        else: 
            better_evalfunc += -0.2 * food

    pacman_position = currentGameState.getPacmanPosition()
    scared_ghosts_distances = []
    scared_ghost_counter = 0
    for ghost in scared_ghosts:
        ghost_position = currentGameState.getGhostPosition(scared_ghost_counter+1)
        pacman_scaredghost_distance = util.manhattanDistance(pacman_position, ghost_position)
        scared_ghosts_distances.append(pacman_scaredghost_distance)
        scared_ghost_counter += 1

    for ghost in scared_ghosts_distances:
        if ghost < 3:
            better_evalfunc += -20 * ghost
        else:
            better_evalfunc += -10 * ghost

    pacman_position = currentGameState.getPacmanPosition()
    attack_ghosts_distances = []
    attack_ghosts_counter = 0
    for ghost in attack_ghosts:
        ghost_position = currentGameState.getGhostPosition(scared_ghost_counter+1)
        pacman_attackghost_distance = util.manhattanDistance(pacman_position, ghost_position)
        attack_ghosts_distances.append(pacman_attackghost_distance)
        attack_ghosts_counter += 1

    for ghost in attack_ghosts_distances:
        if ghost < 3:
            better_evalfunc += 3 * ghost
        elif ghost < 7:
            better_evalfunc += 2 * ghost
        else:
            better_evalfunc += 0.5 * ghost

    return better_evalfunc
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
