import railml_parser
import data_formatting
import segment_generator
import route_generator_prep
import route_generator
import route_file_generator_prep
import route_file_generator
import route_parser
import xml.etree.ElementTree as ET

def finder(timetable_file_path:str, route_data_from_route_parser):
    tree = ET.parse(timetable_file_path)
    root = tree.getroot()

    lineTraffics = []
    for line_element in root.findall('line'):
        # Make stop boolean
        stop_value = line_element.get('stop')
        stop_boolean = stop_value.lower() == 'true' 
        for route in route_data_from_route_parser:
            if route['start'] == line_element.get('start') and route['end'] == line_element.get('end'):
                need_route = route['id']
        line = {'id': line_element.get('id'),
                'name': line_element.get('name'),
                'start': line_element.get('start'),
                'end': line_element.get('end'),
                'route': need_route,
                'timeFrom': line_element.get('timeFrom'),
                'timeTo': line_element.get('timeTo'),
                'freq': line_element.get('freq'),
                'stop': str(stop_boolean),
                'priority': line_element.get('priority')}
        
        lineTraffics.append(line)
    new_root = ET.Element("lineTraffics")
    for i in lineTraffics:
        new_line = ET.SubElement(new_root, "line")
        new_line.set("id", i['id'])
        new_line.set("name", i['name'])
        new_line.set("start", i['start'])
        new_line.set("end", i['end'])
        new_line.set("route", i['route'])
        new_line.set("timeFrom", i['timeFrom'])
        new_line.set("timeTo", i['timeTo'])
        new_line.set("freq", i['freq'])
        new_line.set("stop", i['stop'])
        new_line.set("priority", i['priority'])
    new_tree = ET.ElementTree(new_root)
    new_tree.write(f"{timetable_file_path}_after_finder.xml", encoding="utf-8", xml_declaration=True)

# Example test
if __name__ == "__main__":
    tracks_info = railml_parser.parser('3Tracks.railml.xml')
    [track_data, connection_data, circuitBorder_data] = data_formatting.data_formatting(tracks_info)
    pairs = segment_generator.pairing(connection_data, circuitBorder_data)
    [start_n_end, up_graph, down_graph, start_n_end_dir] = route_generator_prep.generator_prep(track_data, pairs)
    paths = route_generator.generator(start_n_end, start_n_end_dir, up_graph, down_graph)
    result = route_file_generator_prep.file_generator_prep(paths, pairs, start_n_end_dir, track_data)
    route_file_generator.generator(tracks_info, track_data, circuitBorder_data, result, "3Tracks_result")
    routes = route_parser.parser('3Tracks_result.xml')
    finder('3Tracks_flow.xml', routes)