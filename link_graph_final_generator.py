def generator(areas):
    link_graph = {}
    
    for i, area in enumerate(areas):
        link_graph[i] = []
        # 查找与当前区域相邻的其他区域
        for j, other_area in enumerate(areas):
            if i != j:
                # 如果两个区域相邻，则将相邻区域的索引添加到列表中
                if area[1] == other_area[0] or area[0] == other_area[1]:
                    link_graph[i].append(j)
    
    return link_graph