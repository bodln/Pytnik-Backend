import heapq
import json
from itertools import permutations

from pytnik.functions import load_map, permutations

def get_graph(map_name):
    return load_map(map_name)
    
def calculateCost(allPaths, coin_distance):
    pass

class Agent:
    def __init__(self, x, y, file_name):
        pass

def get_agent_steps(agent, map_name):
    coin_distance = load_map(map_name)

    path = agent.get_agent_path(coin_distance)
    steps = [{
        "step": i,
        "to_node": node,
        "from_node": path[i-1] if i > 0 else 0,
        "cost": coin_distance[path[i-1]][node] if i > 0 else 0
    } for i, node in enumerate(path)]

    return steps

def get_agent_by_name(name):
    agents = {
        'Aki': Aki,
        'Jocke': Jocke,
        'Uki': Uki,
        'Micko': Micko
    }

    try:
        agent_class = agents[name]
        return agent_class(0, 0, 'file_name')
    except KeyError:
        raise ValueError(f"Unsupported agent name: {name}")

class Aki(Agent):
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)

    def get_agent_path(self, coin_distance):
        coins = [i for i in range(1, len(coin_distance))]
        
        path = [0]
        
        nextCoin = 0
        path.append(nextCoin)

        while len(coins):
            availCoins = {}
            
            rowCoinsCost = coin_distance[nextCoin]

            for i in coins:
                availCoins[i] = rowCoinsCost[i]

            nextCoin = min(availCoins, key=availCoins.get)
            
            # Add the nearest coin to the path and remove it from the available coins
            path.append(nextCoin)
            coins.remove(nextCoin)

        # Append the starting node 0 to complete the path
        path.append(0)

        # Return the final path for the agent
        return path

class Jocke(Agent):
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)

    def get_agent_path(self, coin_distance):
        path = [i for i in range(1, len(coin_distance))]
        allPaths = permutations(path)
        costs = calculateCost(allPaths, coin_distance)
        minCost = min(costs)
        minCostIndex = costs.index(minCost)

        return [0] + list(allPaths[minCostIndex]) + [0]

def calculateCost(allPaths, coin_distance):
    costs = []

    for path in allPaths:
        path = list(path)
        path.insert(0, 0)
        sum = 0
        
        for i in range(0, (len(path) - 1)):
            sum += coin_distance[path[i]][path[i+1]]
            
        sum += coin_distance[path[len(path) - 1]][0]
        costs.append(sum)

    return costs

class Uki(Agent):
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)

    def get_agent_path(self, coin_distance):
        # Get the number of nodes in the map (excluding the starting node 0)
        n = len(coin_distance)  

        # Define the initial state as a tuple (cost, remaining nodes, current node, path)
        firstNode = (0, n, 0, [0])

        # Initialize a priority queue (min-heap) with the initial state
        listOfNodes = [firstNode]
        heapq.heapify(listOfNodes)

        while len(listOfNodes) != 0:
            # Pop the node with the lowest cost from the priority queue
            curr = heapq.heappop(listOfNodes)

            # If the agent has visited all nodes, return the path
            if len(curr[3]) == (n + 1):
                return curr[3]

            # If the agent has visited all nodes except the starting node, set remaining to [0]
            if len(curr[3]) == n:
                remaining = [0]
            else:
                # Get the remaining nodes that have not been visited
                remaining = [i for i in range(1, n) if i not in curr[3]]

            # Explore possible next nodes and add them to the priority queue
            for i in remaining:
                # Push the next node with updated cost, remaining nodes, current node, and path
                heapq.heappush(listOfNodes, (curr[0] + coin_distance[curr[2]][i], (curr[1] - 1), i, curr[3] + [i]))

        # If no path is found, return an empty list
        return []


class Micko(Agent):
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)

    def get_agent_path(self, coin_distance):
        path = [i for i in range(1, len(coin_distance))]
        # Number of coins on map
        n = len(coin_distance)
        firstNode = (0, n, 0, [0], 0) 
        # 0 - distance from start to this node, 
        # 1 - number of unvisited nodes, 
        # 2 - which number node it is,
        # 3 - array of visited nodes,
        # 4 - distance from start to this node but without the heuristic value
        listOfNodes = [firstNode]
        heapq.heapify(listOfNodes)

        while (len(listOfNodes) != 0):
            curr = heapq.heappop(listOfNodes)
            
            if (len(curr[3]) == (n + 1)):
                return curr[3]
            if (len(curr[3]) == n):  
                remaining = [0]
            else:
                remaining = [i for i in range(1, n) if i not in curr[3]]
                
            expandAndCalculate(remaining, listOfNodes, curr, coin_distance, n)

def expandAndCalculate(remaining, listOfNodes, curr, coin_distance, n):
    matrix = scaleMatrix(curr, n, coin_distance)

    if not len(matrix):
        heur = 0
    else:
        heur = primsAlgorithm(matrix)
    for i in remaining:
        heapq.heappush(listOfNodes, (curr[4] + coin_distance[curr[2]][i] + heur, (curr[1] - 1), i, curr[3] + [i], curr[4] + coin_distance[curr[2]][i]))

def scaleMatrix(curr, n, coin_distance):
    newlist = []
    selected = [i for i in range(1, n) if i not in curr[3]]

    if not len(selected):
        return []
    
    selected.append(0)
    selected.sort()

    for i in selected:
        subList = []
        for j in selected:
            subList.append(coin_distance[i][j])
        newlist.append(subList)

    return newlist

def primsAlgorithm(matrix):
    n = len(matrix)  # Number of nodes
    nodes = [0] * n  # List to keep track of selected nodes in the MinimumSpanningTree
    number_of_edges = 0  
    nodes[0] = True 
    sum = 0  # Variable to store the total weight of the MST

    # Iterate until the MST has n-1 number_of_edges (where n is the number of nodes)
    while (number_of_edges < n - 1):
        minimum = 99999999
        a = 0
        b = 0

        # Iterate over the selected nodes in the MST
        for m in range(n):
            if nodes[m]:
                # Check adjacent nodes that are not yet selected
                for i in range(n):
                    if (not nodes[i]) and matrix[m][i]:
                        # Update minimum if a smaller edge weight is found
                        if minimum > matrix[m][i]:
                            minimum = matrix[m][i]
                            a = m
                            b = i

        # Include the minimum edge in the MST
        sum = sum + matrix[a][b]
        nodes[b] = True
        number_of_edges = number_of_edges + 1

    return sum

