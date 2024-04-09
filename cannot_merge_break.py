import usage_matrix_gererator
import route_selection
from itertools import combinations
def devider(can_merge, cannot_merge, single, connection, close_unarrange, circuit_relation, circuits, routes, tracks_info, lineTraffics):
    # Try to devide cannot_merge to see if smaller area can be merged
    for item in cannot_merge:
        # If the area is leq 2 min areas, then direct add them to single
        if len(item) <= 2:
            for node in item:
                single.append(node)
        else:
            # Else get conbinations
            possibles = []
            for r in range(1, len(item) + 1):
                possibles.extend(combinations(item, r))
            # Delete possibles have not connected area
        feasible_possibles = []
        for possible in possibles:
            connected = True
            if len(possible) >= 2:
                for i in range(len(possible)-1):
                    if possible[i+1] not in connection[possible[i]]:
                        connected = False
                        break
            if connected:
                feasible_possibles.append(possible)
        # Order feasible_possibles by length of each element and delete single area element
        feasible_possibles = sorted(feasible_possibles, key=len, reverse=True)
        feasible_possibles = [nodes for nodes in feasible_possibles if len(nodes) > 1]
        # Try every feasible possible, from possible with most areas to least
        no_match = True
        for possible in feasible_possibles:
            standard = close_unarrange[possible[0]]
            # Get cancelled train with possible and see if same as single area
            closed_border = []
            for area in possible:
                for i in range(len(circuit_relation)):
                    if [area] == circuit_relation[i]:
                        closed_border.append(circuits[i][0])
            new_routes = []
            for route in routes:
                alts = []
                for alternative in route['alternatives']:
                    count = 0
                    for node in alternative['nodes']:
                        if node not in closed_border:
                            count = count +1
                    if count == len(alternative['nodes']):
                        alts.append(alternative)
                new_route = {'id': route['id'],
                            'name': route['name'],
                            'start': route['start'],
                            'end': route['end'],
                            'alternatives': alts}
                new_routes.append(new_route)
            [circuitBorder, usage, max_traffic] = usage_matrix_gererator.usage_matrix_generator(tracks_info)
            [usage, borderName, linesPath, unarrangable_traffic] = route_selection.route_selection(lineTraffics, new_routes, circuitBorder, usage, max_traffic)
            if unarrangable_traffic == standard:
                # Add mergable area
                can_merge.append(possible)
                no_match = False
                # Add other areas in single
                unique_elem = set(item) ^ set(possible)
                for elem in unique_elem:
                    single.append(elem)
                break
        if no_match:
            for i in item:
                single.append(i)
    single = sorted(single)
    return can_merge, single