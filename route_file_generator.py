import railml_parser
import data_formatting
import segment_generator
import route_generator_prep
import route_generator
import route_file_generator_prep
import xml.etree.ElementTree as ET

def generator(tracks_info, track_data, circuitBorder_data_from_formatting, result_from_prep, name_for_XML_file:str):
    # Set root element
    root = ET.Element("routes")
    # Get openEnd data [begin, end] from data_formatting
    open_end_begin = []; open_end_end = []
    for track in track_data:
        open_end_begin.append(track['entry_from_start_name'])
        open_end_end.append(track['entry_from_end_name'])
    # Get platform position
    platform = []
    for i, track in tracks_info.items():
        if bool(track['platform']):
            temp = track['platform'][0]
            # [[start_x, end_x][start_y, end_y]]
            platform.append([[temp['absPos'], temp['absPos']+temp['length']], [track['track_id'], track['track_id']]])
        else:
            platform.append(None)
    # Main loop
    for i, route in enumerate(result_from_prep):
        # Set <route>
        xml_route = ET.SubElement(root, "route")
        # Set id
        xml_route.set("id", f"{i+1}")
        # Find and set name & start & end
        n_start = route[0][0]
        n_end = route[0][len(route[0])-1]
        for entry in circuitBorder_data_from_formatting:
            if entry['id'] == n_end:
                Y_end = entry['Y']
                X_end = entry['absPos']
            if entry['id'] == n_start:
                Y_start = entry['Y']
                X_start = entry['absPos']
        if float(X_end) == 0:
            end_name = str(open_end_begin[Y_end])
        else:
            end_name = str(open_end_end[Y_end])
        if float(X_start) == 0:
            start_name = str(open_end_begin[Y_start])
        else:
            start_name = str(open_end_end[Y_start])
        # Insert attributes
        xml_route.set("name", f"{start_name}To{end_name}")
        xml_route.set("start", f"{start_name}")
        xml_route.set("end", f"{end_name}")
        for k, alternative in enumerate(route):
            xml_alternative = ET.SubElement(xml_route, "alternative")
            xml_alternative.set("id", f"{k+1}")
            pass_platform = 0
            for j in range(0,len(alternative)-1):
                node1 = alternative[j]
                node2 = alternative[j+1]
                for node in circuitBorder_data_from_formatting:
                    if node['id'] == node1:
                        pos_node1 = [float(node['absPos']), node['Y']]
                    if node['id'] == node2:
                        pos_node2 = [float(node['absPos']), node['Y']]
                for p in platform:
                    if p is not None:
                        if [pos_node1[1], pos_node2[1]] == p[1] or [pos_node2[1], pos_node1[1]] == p[1]:
                            if (pos_node1[0] <= p[0][0] and pos_node2[0] >= p[0][1]) or (pos_node2[0] <= p[0][0] and pos_node1[0] >= p[0][1]):
                                pass_platform = pass_platform + 1
            if pass_platform >= 1:
                xml_alternative.set("platform", "True")
            else:
                xml_alternative.set("platform", "False")
            for node in alternative:
                xml_node = ET.SubElement(xml_alternative, "node")
                xml_node.set("id", node)
    # Write the file
    tree = ET.ElementTree(root)
    tree.write(f"{name_for_XML_file}.xml", encoding="utf-8", xml_declaration=True)
'''
# Example test
tracks_info = railml_parser.parser('Katrineholm.railml.xml')
[track_data, connection_data, circuitBorder_data] = data_formatting.data_formatting(tracks_info)
pairs = segment_generator.pairing(connection_data, circuitBorder_data)
[start_n_end, up_graph, down_graph, start_n_end_dir] = route_generator_prep.generator_prep(track_data, pairs)
paths = route_generator.generator(start_n_end, start_n_end_dir, up_graph, down_graph)
result = route_file_generator_prep.file_generator_prep(paths, pairs, start_n_end_dir, track_data)
generator(tracks_info, track_data, circuitBorder_data, result, "example")
'''