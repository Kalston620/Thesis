This file is to state function and the execute sequence of each file
# railml_parser:
To parser RailML file, output the track info
## Input: RailML file path
## Output: Track info
## Need: xml.etree.ElementTree

# find_connection:
To find the position of the other end of the switch, do not relay on another file, but only used in plot files
## Input: switches['connection'] in track_info, list of all swithch connection with their coordinates.
## Output: X and Y of the other end of the switch
## Need: None, but only used in plot files

# layout_plot:
Plot the layout based on railml file, this one will plot track, switch link, track circuit border position, switch position, detector position etc.
## Input: tracks_info (output of railml_parser)
## Output: No data, but payout figure
## Need: matplotlib.pyplot, railml_parser, find_connection

# layout_plot_track_only:
Same function as layout_plot, but only plot track and switch connection layout
## Input: tracks_info (output of railml_parser)
## Output: No data, but payout figure
## Need: matplotlib.pyplot, railml_parser, find_connection

# route_parser:
To parser route XML file
## Input: route xml file path
## Output: routes (including all alternatives of path from one end to another)
## Need: xml.etree.ElementTree

# TimeTable_parser:
To parser timetable XML file
## Input: timetable XML file path
## Output: lineTraffics (including all traffic flows from the xml file)
## Need: xml.etree.ElementTree

# usage_matrix_generator:
Generate a all 0 matrix, size of number of track circuit border * 24, to store the usage data of the track. Also decides max allowed traffic for each point
## Input: tracks_info (output of railml_parser)
## Output: circuitBorder (including name, y and x of the track circuit border), usage (matrix), max_traffic
## Need: None, but need to be used before route_selection

# route_selection:
Based on lineTraffics, routes, circuitBorder, usage, max_traffic, decided which alternative the traffic will use, and return with usage of each border at each time (in matrix), borderName (same sequence as usage) and lines_path (including id of traffic, id of route and id of alternative)
## Input: lineTraffics, routes, circuitBorder, usage, max_traffic
## Output: usage, borderName, lines_path
## Need: railml_parser, usage_matrix_gererator, route_parser, TimeTable_parser (Not needed as import but need those's output as input)

# route_visualization:
To plot the selected route for each traffic, will generate as much figures as the number of traffic
## Input: tracks_info (output of railml_parser), routes, lines_path, circuitBorder
## Output: No data, but figures
## Need: railml_parser, usage_matrix_gererator,route_parser, TimeTable_parser, route_selection, layout_plot_track_only, matplotlib.pyplot (Execute this after route_selection)

# data_formatting:
Extract data from the output of railml_parser and format it into needed data form for route generating
## Input: tracks_info (output of railml_parser)
## Output: track_data, connection_data, circuitBorder_data
## Need: railml_parser

# segment_generator:
pair the track circuit border into pair, reportsent as the smallest segement
## Input: connection_data and circuitBorder_data from data_formatting
## Output: pairs
## Need: None, but need to run data_formatting first

# route_dfs:
Use Deep First Search to find all possible alternatives in a route
## Input: graph, start, end, path=None, all_paths=None
## Output: all_paths
## Need: None, only used in route_generator

# route_generator_prep:
Data preperation for route_generator, need to run before route_generator.
## Input: track_data from data_formatting, pairs from segement_generator
## Output: start_n_end_index, up_graph_out, down_graph_out, start_n_end_dir
## Need: None, but need to run data_formatting and segement_generator first

# route_generator:
generate all possible route in the station. Note: only consider line traffic, no turn around, no stop for lone time etc.
## Input: start_n_end, start_n_end_dir, up_graph, down_graph from prep
## Output: total_path
## Need: route_dfs, run after route_generator_prep

# route_file_generator_prep:
Sort needed data by position order, % of running same direction as track main direction etc.
# Input: total_path from route_generator, pairs from segment generator, start_n_end_dir from route_generator_prep, tracks_data from data_formatting
# Output: sorted_result
# Need: None, but need to run route_generator, segment generator, route_generator_prep, data_formatting first

# route_file_generator:
Generate route xml file, including all routes from different starting and ending point in station, as well as all alternatives in the route
# Input: tracks_info from railml_parser, track_data from data_formatting, circuitBorder_data from data_formatting, result_from_prep, name_for_XML_file:str
# Output: None in command window, but the route xml file
# Need: xml.etree.ElementTree, also run after railml_parser, data_formatting, segment_generator, route_generator_prep, route_generator, route_file_generator_prep, route_file_generator

# timetable_route_finder:
Add route that traffic needs into timetable xml file
## Input: timetable file path, route data from route_parser
## Output: None in command window, but a new timetable xml file with route in it
## Need: xml.etree.ElementTree as ET, run after route_file_generator -> route_parser