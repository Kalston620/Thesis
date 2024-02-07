import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

def parse_railml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    tracks = root.find('.//{http://www.railml.org/schemas/2013}tracks')

    track_data = {}
    switches = {}
    connections = []

    for track_elem in tracks.findall('{http://www.railml.org/schemas/2013}track'):
        track_name = track_elem.get('name')
        track_topology = track_elem.find('{http://www.railml.org/schemas/2013}trackTopology')
        track_data[track_name] = []

        for elem in track_topology:
            if elem.tag == '{http://www.railml.org/schemas/2013}trackBegin':
                pos = float(elem.get('pos'))
                abs_pos = float(elem.get('absPos'))
                track_data[track_name].append(('begin', pos, abs_pos))

            elif elem.tag == '{http://www.railml.org/schemas/2013}trackEnd':
                pos = float(elem.get('pos'))
                abs_pos = float(elem.get('absPos'))
                track_data[track_name].append(('end', pos, abs_pos))

            elif elem.tag == '{http://www.railml.org/schemas/2013}switch':
                switch_id = elem.get('id')
                pos = float(elem.get('pos'))
                abs_pos = float(elem.get('absPos'))
                direction = elem.get('dir')
                switches[switch_id] = {'pos': pos, 'abs_pos': abs_pos, 'direction': direction}
                track_data[track_name].append(('switch', pos, abs_pos, switch_id))

            elif elem.tag == '{http://www.railml.org/schemas/2013}connections':
                for connection_elem in elem.findall('{http://www.railml.org/schemas/2013}connection'):
                    connection_id = connection_elem.get('id')
                    ref = connection_elem.get('ref')
                    connections.append((connection_id, ref))

    return track_data, switches, connections

def draw_railway(track_data, switches, connections):
    fig, ax = plt.subplots()

    track_offset = 0

    for track_name, points in track_data.items():
        x_vals = [point[1] + track_offset for point in points]
        y_vals = [point[2] for point in points]
        ax.plot(x_vals, y_vals, label=track_name)
        track_offset += 100  # Adjust this value based on your preference for track separation

    for switch_id, switch_data in switches.items():
        pos = switch_data['pos']
        abs_pos = switch_data['abs_pos']
        direction = switch_data['direction']
        if direction == 'up':
            ax.plot(pos, abs_pos, 'ro', markersize=10, label='Switch ' + switch_id)
        elif direction == 'down':
            ax.plot(pos, abs_pos, 'bo', markersize=10, label='Switch ' + switch_id)

    for connection_id, ref in connections:
        for track_name, points in track_data.items():
            for i in range(len(points) - 1):
                if points[i][0] == 'begin' and points[i + 1][0] == 'begin':
                    if points[i + 1][3] == ref:
                        switch_pos = [switch_data['pos'] + track_offset, switch_data['abs_pos']]
                        track_pos = [points[i][1] + track_offset, points[i + 1][1] + track_offset, points[i + 1][1] + track_offset]
                        track_abs_pos = [points[i][2], points[i + 1][2], points[i + 1][2]]
                        ax.plot(switch_pos, track_abs_pos, 'k--', linewidth=2)
                        ax.plot(track_pos, switch_pos, 'k--', linewidth=2)

    ax.legend()
    plt.xlabel('Position')
    plt.ylabel('Absolute Position')
    plt.title('RailML Track Diagram')
    plt.show()

if __name__ == "__main__":
    xml_file = "example-split.railml.xml"
    track_data, switches, connections = parse_railml(xml_file)
    draw_railway(track_data, switches, connections)
