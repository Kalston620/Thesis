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