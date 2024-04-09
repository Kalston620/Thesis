import route_selection
import usage_matrix_gererator

def categorizer(close_unarrange, cancel_connection, circuit_relation, tracks_info, routes, circuits, lineTraffics):
    can_merge = []
    cannot_merge = []
    single = []
    for i in range(len(close_unarrange)):
        closed_border = []
        if len(cancel_connection[i]) >= 1:
            temp = cancel_connection[i]
            temp.append(i)
            temp.sort()
            for j in range(len(close_unarrange)):
                if j == i or j in cancel_connection[i]:
                    for k in range(len(circuit_relation)):
                        if circuit_relation[k] == [j]:
                            closed_border.append(circuits[k][0])
        if closed_border == []:
            print(f'No. {i} from main line area is unique, cannot merge')
            single.append(i)
        else:
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
            print(f'Merged result for No. {i}, with cancelled:\n{unarrangable_traffic}, same as before: {unarrangable_traffic == close_unarrange[i]}')
            if unarrangable_traffic == close_unarrange[i]:
                can_merge.append(temp)
            else:
                cannot_merge.append(temp)
    # Get rid of same items
    can_merge = list(set(tuple(sublist) for sublist in can_merge))
    cannot_merge = list(set(tuple(sublist) for sublist in cannot_merge))
    return can_merge, cannot_merge, single