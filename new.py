def pathCost(path):
    total = 0
    for (node, cost) in path:
        total += cost
    return total, path[-1][0]

def uniformCostSearch(graph, start, goal):
    visitedNodes = []
    queue = [[(start, 0)]]
    while queue:
        queue.sort(key=pathCost)
        path = queue.pop(0)
        node = path[-1][0]
        if node in visitedNodes:
            continue
        visitedNodes.append(node)
        if node in goal:
            return path
        else:
            adjNodes = graph.get(node, [])
            for (node2, cost) in adjNodes:
                newP = path.copy()
                newP.append((node2, cost))
                queue.append(newP)

graph = {
'S': [('A', 2), ('B', 3), ('D', 5)],
'A': [('C', 4)],
'B': [('D', 4)],
'C': [('D', 1), ('G', 2)],
'D': [('G', 5)],
'G': []
}

solution = uniformCostSearch(graph, 'A', ('G','B'))
print('Solution is ', solution)
print('Cost of solution is ', pathCost(solution)[0])