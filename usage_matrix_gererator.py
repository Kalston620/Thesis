from contourpy import max_threads
import railml_parser

def usage_matrix_generator(track_info):
    circuitBorder = []
    # Get needed data
    for track_id, track_item in track_info.items():
        track_id = track_item['track_id']
        for circuit in track_item['circuits']:
            name = circuit['id']
            pos = float(circuit['pos'])
            circuitBorder.append({"Name": name, "Y-axis": track_id, "X_axis": pos})

    # Set List reprtsent usage of each node in time
    rows = len(circuitBorder)
    cols = 24
    usage = [[0 for _ in range(cols)] for _ in range(rows)]

    # Define Maximum Traffic Flow
    max_traffic = 10
    return circuitBorder, usage, max_traffic

'''
# Example Test
track_info = railml_parser.parser('Katrineholm.railml.xml')
[circuitBorder, usage, max_traffic] = usage_matrix_generator(track_info)
print(circuitBorder)
print(usage)
print(max_traffic)
'''