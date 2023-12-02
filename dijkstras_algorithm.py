def dijkstras_algorithm(matrix, start: int, end: int):
    length = len(matrix)
    costs = [None] * length
    costs[start] = 0

    parents = {}
    for i in range(length):
        parents[i] = None
    parents[start] = False

    visited = [False] * length
    while not all(visited):
        current_index = None
        value_current_index = float('inf')
        for i in range(length):
            if not (costs[i] is None):
                if costs[i] < value_current_index and visited[i] is False:
                    current_index = i
                    value_current_index = costs[current_index]
        if current_index is None:
            break
        visited[current_index] = True
        for i in range(length):
            if current_index == i:
                continue
            if not matrix[current_index][i] is None:
                if costs[i] is None or matrix[current_index][i] + value_current_index < costs[i]:
                    costs[i] = matrix[current_index][i] + value_current_index
                    parents[i] = current_index


    last = end
    order = []
    while True:
        order.append(last)
        last = parents[last]
        if last is False:
            break
    order.reverse()
    return order
