import railml_parser
import usage_matrix_gererator
import route_parser
import TimeTable_parser

def route_selection(lineTraffics, routes, circuitBorder, usage, max_traffic):
    # Set a null matrix to store line_id, used_route, used_alternative for plotting
    lines_path = []
    unarrangable_traffic = []
    # Get only name easier for matching
    borderName = [entry['Name'] for entry in circuitBorder]
    # Go through all line in lineTraffics
    for line in lineTraffics:
        line_id = line['id']
        need_route = line['route']
        timeFrom = int(line['timeFrom'])
        timeTo = int(line['timeTo'])
        frequency = int(line['freq'])
        stop = bool(line['stop'])
        # Go through all route in routes to match needed route
        for route in routes:
            route_id = route['id']
            if route_id == need_route:
                alternatives = route['alternatives']
                # Set traffic overload counter back to 0
                overload_time = 0
                # if there is flow_overload, delete it to prevent unexpected break later
                try:
                    if bool(str(flow_overload)):
                        del flow_overload
                except:
                    pass
                # Go through all alternative in alternatives, to try if traffic can use this alternative
                for alternative in alternatives:
                    alternative_id = alternative['id']
                    platform = bool(alternative['platform'])
                    nodes = alternative['nodes']
                    # Check if need to stop
                    if stop:
                        if platform:
                            temp = usage
                            # Go through nodes to check if overload traffic
                            for node in nodes:
                                index = borderName.index(node)
                                node_24h_flow = temp[index]
                                for i in range(timeFrom,timeTo+1):
                                    node_24h_flow[i] = node_24h_flow[i] + frequency
                                    # If overload, return to previous state and jump out
                                    if node_24h_flow[i] > max_traffic:
                                        node_24h_flow[i] = node_24h_flow[i] - frequency
                                        # Put a jump indicator
                                        flow_overload = True
                                        break
                                    else:
                                        flow_overload = False
                                if flow_overload:
                                    break
                                temp[index] = node_24h_flow
                            usage = temp
                            path_data = {'line id': line_id,
                                         'route id': route_id,
                                         'alternative id': alternative_id}
                    try:
                        # If jump indicator is true, add 1 to overload counter
                        if not flow_overload:
                            lines_path.append(path_data)
                            break
                        else:
                            overload_time = overload_time + 1
                    except NameError:
                        # Need platfrom, but alternative does not have platfrom
                        overload_time = overload_time + 1
                # If overload counter bigger or equal to number of alternatives, traffic cannot be fit in, print error messange
                if overload_time >= len(alternatives):
                    # If traffic only last 1 hour, cannot be added, else maybe part of the traffic can be added in
                    if timeTo - timeFrom == 0:
                        print(f"line id '{line_id}' in timetable cannot be added in, as flow overload!")
                        unarrangable_traffic.append(line_id)
                    else:
                        print(f"line id '{line_id}' in timetable cannot be added in, as flow overload! But consider break this line traffic into smaller time period!")
                        unarrangable_traffic.append(line_id)
    return usage, borderName, lines_path, unarrangable_traffic
                        
'''
# Example test
lineTraffics = TimeTable_parser.parser('test_timetable.xml')
routes = route_parser.parser('Katrineholm_Route.xml')
track_info = railml_parser.parser('Katrineholm.railml.xml')
[circuitBorder, usage, max_traffic] = usage_matrix_gererator.usage_matrix_generator(track_info)
[usage, borderName, linesPath, unarrangable_traffic] = route_selection(lineTraffics, routes, circuitBorder, usage, max_traffic)
for i in range(0, len(borderName)):
    print(f"{borderName[i]}: {usage[i]}\n")
a = []; b = []; c = []
for i in range(0, len(linesPath)):
    a.append(linesPath[i]['line id'])
    b.append(linesPath[i]['route id'])
    c.append(linesPath[i]['alternative id'])
for j in range(0,len(a)):
    print(f"{a[j]}, {b[j]}, {c[j]}")
print(unarrangable_traffic)
'''