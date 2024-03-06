def DFS(graph, start, end, path=[]):
    path = path + [start]
    
    if start == end:
        return path
    
    if start not in graph:
        return None
    
    for neighbor in graph[start]:
        if neighbor not in path:
            new_path = DFS(graph, neighbor, end, path)
            if new_path:
                return new_path
    
    return None

'''
# Example Test
graph = {
    'A': ['B', 'C'],
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

if result:
    print(result)
'''