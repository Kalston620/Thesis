import railml_parser
import data_formatting
import segment_generator

def generator_prep(track_data, pairs):
    start_n_end = []
    first_coor = []
    second_coor = []
    start_n_end_index = []
    up_graph = []
    down_graph = []
    start_n_end_dir = []
    # Get possible start and end coordinate
    for track in track_data:
        if track['Direction'] == 'up' and track['entry_from_end']:
            start = [track['Position End'], track['Y']]
            for track1 in track_data:
                if track1['Direction'] == 'up' and track1['entry_from_start']:
                    end = [track1['Position Start'], track1['Y']]
                    start_n_end.append([end, start])
        elif track['Direction'] == 'down' and track['entry_from_start']:
            start = [track['Position Start'], track['Y']]
            for track1 in track_data:
                if track1['Direction'] == 'down' and track1['entry_from_end']:
                    end = [track1['Position End'], track1['Y']]
                    start_n_end.append([end, start])

    for s_n_e in start_n_end:
        if s_n_e[0][0] == 0:
            start_n_end_dir.append('up')
        else:
            start_n_end_dir.append('down')
    # Get coordinate for all segments
    for pair in pairs:
        first_coor.append([float(pair[0]['absPos']), pair[0]['Y']])
        second_coor.append([float(pair[1]['absPos']), pair[1]['Y']])
    # Match coordinate
    for start_end in start_n_end:
        first_target = [index for index, sublist in enumerate(first_coor) if sublist == start_end[0]] or [index for index, sublist in enumerate(second_coor) if sublist == start_end[0]]
        second_target = [index for index, sublist in enumerate(second_coor) if sublist == start_end[1]] or [index for index, sublist in enumerate(first_coor) if sublist == start_end[1]]
        start_n_end_index.append([first_target,second_target])
    
    # Route graph
    for f_coor in second_coor:
        target = []
        target = [index for index, sublist in enumerate(first_coor) if sublist == f_coor]
        up_graph.append(target)
    for f_coor in first_coor:
        target = []
        target = [index for index, sublist in enumerate(second_coor) if sublist == f_coor]
        down_graph.append(target)

    up_graph_out = {}
    down_graph_out = {}


    for i, neighbors in enumerate(up_graph):
        up_graph_out[i] = neighbors
    for i, neighbors in enumerate(down_graph):
        down_graph_out[i] = neighbors
    
    return start_n_end_index, up_graph_out, down_graph_out, start_n_end_dir

'''
# Example test
tracks_info = railml_parser.parser('Katrineholm.railml.xml')
[track_data, connection_data, circuitBorder_data] = data_formatting.data_formatting(tracks_info)
pairs = segment_generator.pairing(connection_data, circuitBorder_data)
[start_n_end, up_graph, down_graph, start_n_end_dir] = generator_prep(track_data, pairs)
#print(start_n_end)
print(up_graph); print(down_graph); print(start_n_end); print(start_n_end_dir)
'''