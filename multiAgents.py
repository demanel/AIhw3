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
import random, util, itertools

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.
    """


    def getAction(self, gameState):
        """
        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        This evaluation function is not particularly good; using information
        from the game state would allow it to be much better, although still
        not as good as an agent that plans. You may find the information listed
        below helpful in later parts of the project (e.g., when designing
        an evaluation function for your planning agent).
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState):
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
        """
        "*** YOUR CODE HERE ***"
        agents = gameState.getNumAgents()

        legalActions = gameState.getLegalActions(0)
        nextStates = {move: gameState.generateSuccessor(0, move) for move in legalActions}
        nextScores = {move: self.getScoreForDecisionNode(nextStates[move], agents) for move in legalActions}

        bestScore = max(nextScores.values())
        bestMoves = [index for index in nextScores.keys() if nextScores[index] == bestScore]
        chosenMove = random.choice(bestMoves)
        return chosenMove
        # util.raiseNotDefined()

    def getScoreForDecisionNode(self, gameState, agents = 1, round = 1):
        agent = round % agents
        depth = round // agents

        if agents * self.depth == round:
            # We are at the terminal nodes, so we need to compute actual scores here.
            return self.evaluationFunction(gameState)
        else:
            legalActions = gameState.getLegalActions(agent)
            nextStates = {move: gameState.generateSuccessor(agent, move) for move in legalActions}
            scores = {move: self.getScoreForDecisionNode(nextStates[move], agents, round + 1) for move in legalActions}

            if len(scores) == 0:
                return self.evaluationFunction(gameState)
            bestScore = max(scores.values()) if agent == 0 else min(scores.values())
            return bestScore

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        agents = gameState.getNumAgents()
        alpha = float("-inf")
        beta = float("inf")
        val = float("-inf")

        legalActions = gameState.getLegalActions(0)
        nextStates = {move: gameState.generateSuccessor(0, move) for move in legalActions}
        nextScores = {}
        for move in legalActions:
            res = self.minValue(nextStates[move], alpha, beta)
            val = max(val, res)
            alpha = max(alpha, val)
            nextScores[move] = res

        bestMoves = [index for index in nextScores.keys() if nextScores[index] == alpha]
        chosenMove = random.choice(bestMoves)
        return chosenMove

    def minValue(self, gameState, alpha, beta, round = 1):
        val = float("inf")

        agents = gameState.getNumAgents()
        agent = round % agents
        depth = round // agents

        if depth == self.depth or len(gameState.getLegalActions(agent)) == 0:
            val = self.evaluationFunction(gameState)
            return val

        nextRound = round + 1
        nextAgent = nextRound % agents

        legalActions = gameState.getLegalActions(agent)
        for action in legalActions:
            child = gameState.generateSuccessor(agent, action)
            childVal = self.maxValue(child, alpha, beta, nextRound) if nextAgent == 0 else self.minValue(child, alpha, beta, nextRound)
            val = min(val, childVal)

            if val < alpha:
                return val
            beta = min(beta, val)

        return val

    def maxValue(self, gameState, alpha, beta, round = 1):
        val = float("-inf")

        agents = gameState.getNumAgents()
        agent = round % agents
        depth = round // agents

        if depth == self.depth or len(gameState.getLegalActions(agent)) == 0:
            val = self.evaluationFunction(gameState)
            return val

        nextRound = round + 1
        nextAgent = nextRound % agents

        legalActions = gameState.getLegalActions(agent)
        for action in legalActions:
            child = gameState.generateSuccessor(agent, action)
            childVal = self.maxValue(child, alpha, beta, nextRound) if nextAgent == 0 else self.minValue(child, alpha, beta, nextRound)
            val = max(val, childVal)

            if val > beta:
                return val
            alpha = max(alpha, val)

        return val

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        agents = gameState.getNumAgents()

        legalActions = gameState.getLegalActions(0)
        nextStates = {move: gameState.generateSuccessor(0, move) for move in legalActions}
        nextScores = {move: self.getScoreForDecisionNode(nextStates[move], agents) for move in legalActions}

        bestScore = max(nextScores.values())
        bestMoves = [index for index in nextScores.keys() if nextScores[index] == bestScore]
        chosenMove = random.choice(bestMoves)
        return chosenMove

        # util.raiseNotDefined()

    def getScoreForDecisionNode(self, gameState, agents = 1, round = 1):
        agent = round % agents
        depth = round // agents

        if agents * self.depth == round:
            # We are at the terminal nodes, so we need to compute actual scores here.
            return self.evaluationFunction(gameState)
        else:
            legalActions = gameState.getLegalActions(agent)
            nextStates = {move: gameState.generateSuccessor(agent, move) for move in legalActions}
            scores = {move: self.getScoreForDecisionNode(nextStates[move], agents, round + 1) for move in legalActions}

            if len(scores) == 0:
                return self.evaluationFunction(gameState)
            bestScore = max(scores.values()) if agent == 0 else float(sum(scores.values()) / float(len(scores)))
            return bestScore

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
