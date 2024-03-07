def DFS(graph, start, end, path=None, all_paths=None):
    if path is None:
        path = []
    if all_paths is None:
        all_paths = []

    path = path + [start]

    if start == end:
        all_paths.append(path.copy())
        return all_paths

    if start not in graph:
        return None

    for neighbor in graph[start]:
        if neighbor not in path:
            DFS(graph, neighbor, end, path, all_paths)

    return all_paths

'''
# Example test
graph = {
    'A': ['B', 'C', 'I'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F', 'G'],
    'D': ['B'],
    'E': ['B', 'H'],
    'F': ['C'],
    'G': ['C', 'I'],
    'H': ['E'],
    'I': ['G']
}

start_node = 'A'
end_node = 'I'

result = DFS(graph, start_node, end_node)

print(result)
'''