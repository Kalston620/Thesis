import railml_parser
import data_formatting
import segment_generator
import route_generator_prep
import route_dfs

def generator(start_n_end, start_n_end_dir, up_graph, down_graph):
    total_path = []
    for i in range(0,len(start_n_end_dir)):
        if start_n_end_dir[i] == 'up':
            start = start_n_end[i][0][0]
            end = start_n_end[i][1][0]
            graph = up_graph
        elif start_n_end_dir[i] == 'down':
            start = start_n_end[i][0][0]
            end = start_n_end[i][1][0]
            graph = down_graph
        else:
            print('start_n_end_dir error!')
            break
        path = []; paths = []
        paths = route_dfs.DFS(graph, start, end, path, paths)
        total_path.append(paths)
    return total_path


# Example test
tracks_info = railml_parser.parser('Katrineholm.railml.xml')
[track_data, connection_data, circuitBorder_data] = data_formatting.data_formatting(tracks_info)
pairs = segment_generator.pairing(connection_data, circuitBorder_data)
[start_n_end, up_graph, down_graph, start_n_end_dir] = route_generator_prep.generator_prep(track_data, pairs)
paths = generator(start_n_end, start_n_end_dir, up_graph, down_graph)
print(paths)