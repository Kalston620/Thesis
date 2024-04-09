def generator(areas):
    link_graph = {}
    
    for i, area in enumerate(areas):
        link_graph[i] = []
        # Find other nabiour areas
        for j, other_area in enumerate(areas):
            if i != j:
                # Add to graph if found
                if area[1] == other_area[0] or area[0] == other_area[1]:
                    link_graph[i].append(j)
    
    return link_graph