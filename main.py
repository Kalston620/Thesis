from matplotlib import pyplot as plt
import numpy as np
import railml_parser
import min_area_generator
import route_parser
import TimeTable_parser
import area_merge
import data_formatting
import segment_generator
import route_generator_prep
import link_graph_final_generator
import min_area_categorize
import cannot_merge_break
import layout_plot_track_only
import timetable_route_finder
import route_file_generator
import route_file_generator_prep
import route_generator
import route_selection
import route_visualization
import usage_matrix_gererator

file_path = '3Tracks.railml.xml'
route_file_path = '3Tracks_route'
flow_file_path = '3Tracks_flow.xml'
# Start from parse the infra data
tracks_info = railml_parser.parser(file_path)
[track_data, connection_data, circuitBorder_data] = data_formatting.data_formatting(tracks_info)
pairs = segment_generator.pairing(connection_data, circuitBorder_data)
[start_n_end, up_graph, down_graph, start_n_end_dir] = route_generator_prep.generator_prep(track_data, pairs)
main_line_area, connection, switch_area, switch_connection, switch_cross = min_area_generator.generator(tracks_info)
paths = route_generator.generator(start_n_end, start_n_end_dir, up_graph, down_graph)
result = route_file_generator_prep.file_generator_prep(paths, pairs, start_n_end_dir, track_data)
route_file_generator.generator(tracks_info, track_data, circuitBorder_data, result, route_file_path)
# Generate the route file
route_file_path = route_file_path + '.xml'
routes = route_parser.parser(route_file_path)
# Add assigned route to flow file
timetable_route_finder.finder(flow_file_path, routes)
flow_file_path_after_finder = flow_file_path + '_after_finder.xml'
# Parse flow file
lineTraffics = TimeTable_parser.parser(flow_file_path_after_finder)
# Visualization before close segments
[circuitBorder, usage, max_traffic] = usage_matrix_gererator.usage_matrix_generator(tracks_info)
[usage, borderName, lines_path, unarrangable_traffic] = route_selection.route_selection(lineTraffics, routes, circuitBorder, usage, max_traffic)
route_visualization.visualization(tracks_info, routes, lines_path, circuitBorder)

main_line_close_unarrange, cancel_connection, switch_close_unarrange, cancel_connection_switch, circuit_line_relation, circuit_switch_relation, circuits = area_merge.merger(main_line_area, connection, switch_area, switch_connection, switch_cross, tracks_info, routes, lineTraffics)

# Categorize min areas: same behaviour & can be merged, same behaviour & cannot be merged, single area
[can_merge, cannot_merge, single] = min_area_categorize.categorizer(main_line_close_unarrange, cancel_connection, circuit_line_relation, tracks_info, routes, circuits, lineTraffics)
#print(f'{can_merge}\n{cannot_merge}\n{single}')
if cannot_merge != []:
    [can_merge, single] = cannot_merge_break.devider(can_merge, cannot_merge, single, connection, main_line_close_unarrange, circuit_line_relation, circuits, routes, tracks_info, lineTraffics)
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
can_merge_main = can_merge
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
#print(f'{can_merge}\n{cannot_merge}\n{single}')
if cannot_merge != []:
    [can_merge, single] = cannot_merge_break.devider(can_merge, cannot_merge, single, switch_connection, switch_close_unarrange, circuit_switch_relation, circuits, routes, tracks_info, lineTraffics)
# Consider crossing switch pair, and delete switch that is in final
switch_pair = []
for i in range(len(switch_cross)):
    pair = switch_cross[i]
    if pair != []:
        pair.append(i)
        pair = sorted(pair)
    for switch in pair:
        if switch in single:
            single.remove(switch)
        else:
            temp = []
            for group in can_merge:
                if switch in group:
                    if len(group) <= 2:
                        single.append(group[1] if group[0] == switch else group[0])
                        group = ()
                    else:
                        idx = group.index(switch)
                        group = group[:idx] + group[idx+1:]
                if group != ():
                    temp.append(group)
            can_merge = temp
    if tuple(pair) not in switch_pair and pair != []:
        switch_pair.append(tuple(pair))
final_switch = switch_pair
# See if can_merge actually can merge (based on start and end of switch is in same main line area)
temp = []
for group in can_merge:
    group_connection = []
    for switch in group:
        group_connection.append(switch_connection[switch])
    unique_tuples = set(tuple(sublist) for sublist in group_connection)
    unique_group_connection = [list(t) for t in unique_tuples]
    if len(unique_group_connection) == len(group_connection):
        # No one can be merged
        for switch in group:
            final_switch.append(switch)
    elif len(unique_group_connection) == 1:
        # All can be merged
        final_switch.append(group)
    else:
        # Some can be merged
        for conn in unique_group_connection:
            position = [index for index, connection in enumerate(group_connection) if connection == conn]
            if len(position) == 1:
                final_switch.append(group[position])
            else:
                temp = []
                for pos in position:
                    temp.append(group[pos])
                final_switch.append(tuple(temp))
# Sort final_switch and add single
for item in single:
    final_switch.append(item)
final_switch = sorted(final_switch, key=lambda x: 1 if isinstance(x, int) else len(x))
# Consider the relation between switch and main line area
switch_main_relation = [[] for _ in range(len(final_switch))]
for i in range(len(final_switch)):
    item = final_switch[i]
    if isinstance(item, int):
        start = switch_connection[item][0]
        end = switch_connection[item][1]
        for j in range(len(can_merge_main)):
            group = can_merge_main[j]
            if start in group and end in group:
                switch_main_relation[i] = [j]
    else:
        for switch in item:
            temp = []
            b_sign = False
            start = switch_connection[switch][0]
            end = switch_connection[switch][1]
            for j in range(len(can_merge_main)):
                group = can_merge_main[j]
                if start in group and end in group:
                    temp.append(j)
                else:
                    b_sign = True
                    break
            if b_sign:
                break
        if len(temp) == len(item) and len(list(set(temp))) == 1:
            switch_main_relation[i] = [j]
#TODO: find real connection between switch and main area based on switch_main_relation and final
same_color_min_area = {}
same_color_final = {}
for i in range(len(switch_main_relation)):
    item = switch_main_relation[i]
    if item != []:
        group = can_merge_main[item[0]]
        switch_group = final_switch[i]
        if not isinstance(switch_group, int):
            switch_group = switch_group[0]
        conn = switch_connection[switch_group]
        temp = []
        temp1 = []
        for item in conn:
            if item in final:
                # Then it is a single area
                temp.append(item)
                temp1.append(final.index(item))
            else:
                for area in final:
                    if not isinstance(area, int):
                        if item in area:
                            temp1.append(final.index(area))
                            for j in area:
                                temp.append(j)
        same_color_min_area[final_switch[i]] = temp
        same_color_final[final_switch[i]] = temp1

print(f'Mainline_final:\n{final}\nSwitch_final:\n{final_switch}\nSame block for switch and mainline:\n{same_color_min_area}\nSame block for switch and final:\n{same_color_final}')
# TODO: Write visualization part
layout_plot_track_only.plot_track_layout(tracks_info)
# plot switch in different color
color_store = [[] for _ in range(len(final))]
for item in final_switch:
    if isinstance(item, int):
        # Single situation
        x1 = switch_area[item][0][1]
        x2 = switch_area[item][1][1]
        y1 = switch_area[item][0][0]
        y2 = switch_area[item][1][0]
        color = np.random.rand(3,)
        plt.plot([x1, x2], [y1, y2], color=color)
        # If relate to main line area, store the color
        if item in same_color_final:
            areas = same_color_final[item]
            for area in areas:
                color_store[area] = color
    else: 
        # Group situation
        color = np.random.rand(3,)
        for switch in item:
            x1 = switch_area[switch][0][1]
            x2 = switch_area[switch][1][1]
            y1 = switch_area[switch][0][0]
            y2 = switch_area[switch][1][0]
            plt.plot([x1, x2], [y1, y2], color=color)
        if item in same_color_final:
            areas = same_color_final[item]
            for area in areas:
                color_store[area] = color
# Plot main line area in different color
for i in range(len(final)):
    item = final[i]
    if len(color_store[i]) == 0:
        color =  np.random.rand(3,)
    else:
        color = color_store[i]
    x1 = final_pos[i][0][1]
    x2 = final_pos[i][1][1]
    y1 = final_pos[i][0][0]
    y2 = final_pos[i][1][0]
    plt.plot([x1, x2], [y1, y2], color=color)
# Show plot
plt.show()