import railml_parser
import usage_matrix_gererator
import route_parser
import TimeTable_parser
import route_selection
import layout_plot_track_only
import matplotlib.pyplot as plt

def visualization(tracks_info, routes, lines_path, circuitBorder):
    borderName = [entry['Name'] for entry in circuitBorder]
    for i in range(0, len(lines_path)):
        layout_plot_track_only.plot_track_layout(tracks_info)
        used_route = lines_path[i]['route id']
        used_alternative = lines_path[i]['alternative id']
        for route in routes:
            route_id = route['id']
            if route_id == used_route:
                alternates = route['alternatives']
                for alternative in alternates:
                    alternative_id = alternative['id']
                    if alternative_id == used_alternative:
                        nodes = alternative['nodes']
                        node1 = nodes[0]
                        index1 = borderName.index(node1)
                        [Y1, X1] = [int(circuitBorder[index1]['Y-axis']), int(circuitBorder[index1]['X_axis'])]
                        for j in range(2, len(nodes)):
                            node2 = nodes[j]
                            index2 = borderName.index(node2)
                            [Y2, X2] = [int(circuitBorder[index2]['Y-axis']), int(circuitBorder[index2]['X_axis'])]
                            plt.plot([X1, X2], [Y1, Y2], linestyle='-', color='red', linewidth=3)
                            [Y1, X1] = [Y2, X2]
                        plt.show()

# Example test
tracks_info = railml_parser.parser('Katrineholm.railml.xml')
routes = route_parser.parser('Katrineholm_Route.xml')
[circuitBorder, usage, max_traffic] = usage_matrix_gererator.usage_matrix_generator(tracks_info)
lineTraffics = TimeTable_parser.parser('Katrineholm_TimeTable.xml')
[usage, borderName, lines_path] = route_selection.route_selection(lineTraffics, routes, circuitBorder, usage, max_traffic)
visualization(tracks_info, routes, lines_path, circuitBorder)