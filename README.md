# Thesis Code
## Work Till 8/2-24:
railml_parser.py will read RailML XML file and extract track name, start and end position (only use 'absPos' in XML file), signal name and position, switches name and position, train detectors name and position. All info will stored in 'tracks_info' with an additional 'track_id', which used as y-axis for plotting.

layout_plot.py will read 'tracks_info and then plot all elements. (Not including the actual line for switch yet.)