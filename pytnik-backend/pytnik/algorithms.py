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
    print("get agent")
    print(map_name)
    coin_distance = load_map(map_name)

    path = agent.get_agent_path(coin_distance)
    steps = [{
        "step": i,
        "to_node": node,
        "from_node": path[i-1] if i > 0 else 0, # 0 is the starting node
        "cost": coin_distance[path[i-1]][node] if i > 0 else 0
    } for i, node in enumerate(path)]

    return steps

# Supported algorithms
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

# Aki - Greedy
class Aki(Agent):
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)

    def get_agent_path(self, coin_distance):
        coins = [i for i in range(1, len(coin_distance))]
        path = []
        nextCoin = 0
        path.append(nextCoin)

        while len(coins):
            availCoins = {}
            rowCoinsCost = coin_distance[nextCoin]

            for i in coins:
                availCoins[i] = rowCoinsCost[i]

            nextCoin = min(availCoins, key=availCoins.get)
            path.append(nextCoin)
            coins.remove(nextCoin)

        path.append(0)

        return path

# Jocke - Brute force
class Jocke(Agent):
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)

    def get_agent_path(self, coin_distance):
        path = [i for i in range(1, len(coin_distance))]
        allPaths = permutations(path)
        costs = calculateCost(allPaths, coin_distance)
        minimumCost = min(costs)
        minimumCostIndex = costs.index(minimumCost)

        return [0] + list(allPaths[minimumCostIndex]) + [0]

#
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

# Uki - Branch and bound
class Uki(Agent):
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)

    def get_agent_path(self, coin_distance):
        path = [i for i in range(1, len(coin_distance))]
        n = len(coin_distance) #8
        firstNode = (0, n, 0, [0])

        listOfNodes = [firstNode]
        heapq.heapify(listOfNodes)

        while(len(listOfNodes) != 0):
            curr = heapq.heappop(listOfNodes)

            if (len(curr[3]) == (n + 1)):
                # Found next node
                return curr[3]
            
            if(len(curr[3]) == n):
                # If path has visited all nodes except the last one, it should return to the first one
                remaining = [0]
            else:
                remaining = [i for i in range(1, n) if i not in curr[3]]

            for i in remaining:
                heapq.heappush(listOfNodes, (curr[0] + coin_distance[curr[2]][i], (curr[1] - 1), i, curr[3] + [i]))

        return []

# Micko - A*
class Micko(Agent):
    def __init__(self, x, y, file_name):
        super().__init__(x, y, file_name)

    def get_agent_path(self, coin_distance):
        path = [i for i in range(1, len(coin_distance))]
        n = len(coin_distance)  # 8
        firstNode = (0, n, 0, [0], 0)
        listOfNodes = [firstNode]
        heapq.heapify(listOfNodes)

        while (len(listOfNodes) != 0):
            curr = heapq.heappop(listOfNodes)
            if (len(curr[3]) == (n + 1)):  # Nasli smo putanju sa ciljnim cvorom
                return curr[3]
            if (len(curr[3]) == n):  # Ako je putanja obisla sve sem krajnjeg, treba da se vrati
                remaining = [0]
            else:
                remaining = [i for i in range(1, n) if i not in curr[3]]
            expandAndCalculate(remaining, listOfNodes, curr, coin_distance, n)

def expandAndCalculate(remaining, listOfNodes, curr, coin_distance, n):
    scaledMatrix = scaleMatrix(curr, n, coin_distance)

    if not len(scaledMatrix):
        heur = 0
    else:
        heur = primsAlgorithm(scaledMatrix)
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

def primsAlgorithm(scaledMatrix):
    inf = 2147483647
    n = len(scaledMatrix)
    selected_node = [0] * n
    no_edge = 0
    selected_node[0] = True
    sumAll = 0

    while (no_edge < n - 1):
        minimum = inf
        a = 0
        b = 0

        for m in range(n):
            if selected_node[m]:
                for i in range(n):
                    if((not selected_node[i]) and scaledMatrix[m][i]):
                        if minimum > scaledMatrix[m][i]:
                            minimum = scaledMatrix[m][i]
                            a = m
                            b = i

        sumAll = sumAll + scaledMatrix[a][b]
        selected_node[b] = True
        no_edge = no_edge + 1

    return sumAll
