import railml_parser
import min_area_generator
import route_parser
import TimeTable_parser
import usage_matrix_gererator
import route_selection
import area_merge
import data_formatting
import segment_generator
import route_generator_prep
import link_graph_final_generator
import min_area_categorize
from itertools import combinations

file_path = 'Katrineholm.railml.xml'
tracks_info = railml_parser.parser(file_path)
[track_data, connection_data, circuitBorder_data] = data_formatting.data_formatting(tracks_info)
pairs = segment_generator.pairing(connection_data, circuitBorder_data)
[start_n_end, up_graph, down_graph, start_n_end_dir] = route_generator_prep.generator_prep(track_data, pairs)
main_line_area, connection, switch_area, switch_connection, switch_cross = min_area_generator.generator(tracks_info)
route_file_path = 'example.xml'
routes = route_parser.parser(route_file_path)
lineTraffics = TimeTable_parser.parser('test.xml_after_finder.xml')
main_line_close_unarrange, cancel_connection, switch_close_unarrange, cancel_connection_switch, circuit_line_relation, circuit_switch_relation, circuits = area_merge.merger(main_line_area, connection, switch_area, switch_connection, switch_cross, tracks_info, routes, lineTraffics)

# Categorize min areas: same behaviour & can be merged, same behaviour & cannot be merged, single area
[can_merge, cannot_merge, single] = min_area_categorize.categorizer(main_line_close_unarrange, cancel_connection, circuit_line_relation, tracks_info, routes, circuits, lineTraffics)
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
single = sorted(single)
print(f'Biggest maintenance areas: {can_merge} Note that big areas may not be connected!\nSingle areas: {single}')
# Get maintenance areas that are connected to eachother
link_graph = link_graph_final_generator.generator(main_line_area)
# First add single area into final result
final = single
# Merge the area based on the connection
for areas in can_merge:
    # 1. Try to merge areas with only 2 area
    if len(areas) == 2:
        if areas[1] in link_graph[areas[0]]:
            final.append(areas)
        else:
            final.append(areas[0])
            final.append(areas[1])
    # 2. If there is something wrong, have single area, put it in final
    elif len(areas) == 1:
        final.append(areas[0])
    # 3. areas >= 3 situation
    else:
        while areas:
            area = areas[0]  # Get first area
            used_area = [area]  # Generate used_area
            other_areas = [a for a in areas if a != area]  # Get other area
            for other_area in other_areas:
               if any(other_area in link_graph[a] for a in used_area):
                    used_area.append(other_area)
            if len(used_area) == len(areas):
                # All areas can be merged
                final.append(tuple(areas))
                break
            else:
                final.append(tuple(used_area))
                areas = [area for area in areas if area not in used_area]  # update areas
# Get position
final_pos = []
for areas in final:
    if isinstance(areas, int):
        final_pos.append(main_line_area[areas])
    else:
        x_start_temp = 0
        y_start_temp = 0
        x_end_temp = 0
        y_end_temp = 0
        for area in areas:
            if area == areas[0]:
                x_start_temp = main_line_area[area][0][1]
                y_start_temp = main_line_area[area][0][0]
                x_end_temp = main_line_area[area][1][1]
                y_end_temp = main_line_area[area][1][0]
            else:
                if main_line_area[area][0][1] < x_start_temp:
                    x_start_temp = main_line_area[area][0][1]
                if main_line_area[area][1][1] > x_end_temp:
                    x_end_temp = main_line_area[area][1][1]
        pos = ([y_start_temp, x_start_temp], [y_end_temp, x_end_temp])
        final_pos.append(pos)
#print(f'{final}\n{final_pos}')

# Consider switches
[can_merge, cannot_merge, single] = min_area_categorize.categorizer(switch_close_unarrange, cancel_connection_switch, circuit_switch_relation, tracks_info, routes, circuits, lineTraffics)
print(f'{can_merge}\n{cannot_merge}\n{single}')