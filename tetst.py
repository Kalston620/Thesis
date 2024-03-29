import railml_parser
import min_area_generator
import route_parser
import TimeTable_parser
import usage_matrix_gererator
import route_selection
import area_merge
from itertools import combinations

file_path = 'Katrineholm.railml.xml'
tracks_info = railml_parser.parser(file_path)
main_line_area, connection, switch_area, switch_connection, switch_cross = min_area_generator.generator(tracks_info)
route_file_path = 'example.xml'
routes = route_parser.parser(route_file_path)
lineTraffics = TimeTable_parser.parser('test.xml_after_finder.xml')
main_line_close_unarrange, cancel_connection, switch_close_unarrange, cancel_connection_switch, circuit_line_relation, circuits = area_merge.merger(main_line_area, connection, switch_area, switch_connection, switch_cross, tracks_info, routes, lineTraffics)

# Categorize min areas: same behaviour & can be merged, same behaviour & cannot be merged, single area
can_merge = []
cannot_merge = []
single = []
for i in range(len(main_line_close_unarrange)):
    closed_border = []
    if len(cancel_connection[i]) >= 1:
        temp = cancel_connection[i]
        temp.append(i)
        temp.sort()
        for j in range(len(main_line_close_unarrange)):
            if j == i or j in cancel_connection[i]:
                for k in range(len(circuit_line_relation)):
                    if circuit_line_relation[k] == [j]:
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
        print(f'Merged result for No. {i}, with cancelled:\n{unarrangable_traffic}, same as before: {unarrangable_traffic == main_line_close_unarrange[i]}')
        if unarrangable_traffic == main_line_close_unarrange[i]:
            can_merge.append(temp)
        else:
            cannot_merge.append(temp)
# Get rid of same items
can_merge = list(set(tuple(sublist) for sublist in can_merge))
cannot_merge = list(set(tuple(sublist) for sublist in cannot_merge))
#print(f'{can_merge}\n{cannot_merge}\n{single}')
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
        standard = main_line_close_unarrange[possible[0]]
        # Get cancelled train with possible and see if same as single area
        closed_border = []
        for area in possible:
            for i in range(len(circuit_line_relation)):
                if [area] == circuit_line_relation[i]:
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
print(f'Biggest maintenance areas: {can_merge} Note that big areas may not be connected!\nSingle areas: {single}')
# Get maintenance areas that are connected to eachother
#for area in can_merge:
    