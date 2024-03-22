import railml_parser
import min_area_generator
import route_parser
import TimeTable_parser
import usage_matrix_gererator
import route_selection

def merger(main_line_area, connection, switch_area, switch_connection, switch_cross, tracks_info, routes, result_TimeTable_parser):
    circuits = []
    for track_name, track_info in tracks_info.items():
        y = track_info['track_id']
        for circuit in track_info['circuits']:
            id = circuit['id']
            pos = float(circuit['absPos'])
            circuits.append([id, y, pos])
    #print(circuits, len(circuits))
    # Get which area circuit are in
    circuit_line_relation = []
    circuit_switch_relation = []
    for circuit in circuits:
        border_y = circuit[1]
        border_x = circuit[2]
        temp = []
        for i in range(len(main_line_area)):
            if main_line_area[i][0][0] == border_y:
                if main_line_area[i][0][1] <= border_x <= main_line_area[i][1][1] or main_line_area[i][1][1] <= border_x <= main_line_area[i][0][1]:
                    temp.append(i)
        circuit_line_relation.append(temp)
        temp1 = []
        for j in range(len(switch_area)):
            if switch_area[j][0][0] == border_y and switch_area[j][0][1] == border_x:
                temp1.append(j)
            elif switch_area[j][1][0] == border_y and switch_area[j][1][1] == border_x:
                temp1.append(j)
        circuit_switch_relation.append(temp1)
    #print(circuit_line_relation)
    #print(circuit_switch_relation, len(circuit_switch_relation))
    # Try to arrange the traffic with closed area, get un-arrangable traffic
    # 1. Try main line areas
    main_line_close_unarrange = []
    for i in range(len(main_line_area)):
        # Find which track circuit border must be close
        closed_border = []
        for j in range(len(circuit_line_relation)):
            if circuit_line_relation[j][0] == i:
                closed_border.append(circuits[j][0])
        print(f'\033[91mTry to close main line section {i}, resultion closing border: {closed_border}.\033[0m')
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
        #print(new_routes)
        '''
        for route in new_routes:
            print(f"Route ID: {route['id']}, Name: {route['name']}, Start: {route['start']}, End: {route['end']}")
            for alternative in route['alternatives']:
                print(f"  Alternative ID: {alternative['id']}, Platform: {alternative['platform']}, Nodes: {alternative['nodes']}")
        '''
        [circuitBorder, usage, max_traffic] = usage_matrix_gererator.usage_matrix_generator(tracks_info)
        [usage, borderName, linesPath, unarrangable_traffic] = route_selection.route_selection(lineTraffics, new_routes, circuitBorder, usage, max_traffic)
        main_line_close_unarrange.append(unarrangable_traffic)
    #print(main_line_close_unarrange)
    #for i in range(len(main_line_close_unarrange)):
        #print(f'{i}: {main_line_close_unarrange[i]}')
    # Merge main line area based on same cancelled train'
    cancel_connection = []
    for i in range(len(main_line_close_unarrange)):
        temp = []
        for j in range(len(main_line_close_unarrange)):
            if i==j:
                continue
            if main_line_close_unarrange[i] == main_line_close_unarrange[j]:
                temp.append(j)
        cancel_connection.append(temp)
    #print(cancel_connection)
    # 2. Try switch areas
    switch_close_unarrange = []
    for i in range(len(switch_area)):
        closed_border = []
        for j in range(len(circuit_switch_relation)):
            if circuit_switch_relation[j] == [i]:
                closed_border.append(circuits[j][0])
        print(f'\033[91mTry to close switch {i}, resultion closing border: {closed_border}.\033[0m')
        new_routes_switch = []
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
            new_routes_switch.append(new_route)
        [circuitBorder, usage, max_traffic] = usage_matrix_gererator.usage_matrix_generator(tracks_info)
        [usage, borderName, linesPath, unarrangable_traffic] = route_selection.route_selection(result_TimeTable_parser, new_routes_switch, circuitBorder, usage, max_traffic)
        switch_close_unarrange.append(unarrangable_traffic)
    #print(switch_close_unarrange)
    cancel_connection_switch = []
    for i in range(len(switch_close_unarrange)):
        temp = []
        for j in range(len(switch_close_unarrange)):
            if i==j:
                continue
            if switch_close_unarrange[i] == switch_close_unarrange[j]:
                temp.append(j)
        cancel_connection_switch.append(temp)
    return main_line_close_unarrange, cancel_connection, switch_close_unarrange, cancel_connection_switch

'''
# Example test
file_path = 'Katrineholm.railml.xml'
tracks_info = railml_parser.parser(file_path)
main_line_area, connection, switch_area, switch_connection, switch_cross = min_area_generator.generator(tracks_info)
route_file_path = 'example.xml'
routes = route_parser.parser(route_file_path)
lineTraffics = TimeTable_parser.parser('test.xml_after_finder.xml')
[main_line_close_unarrange, cancel_connection, switch_close_unarrange, cancel_connection_switch] = merger(main_line_area, connection, switch_area, switch_connection, switch_cross, tracks_info, routes, lineTraffics)
'''