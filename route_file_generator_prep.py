import railml_parser
import data_formatting
import segment_generator
import route_generator_prep
import route_generator


def file_generator_prep(total_path, pairs, start_n_end_dir, tracks_data):

    result = []
    # Unpack nodes from pairs
    for index, path in enumerate(total_path):
        direction = start_n_end_dir[index]
        values = []
        for alt_index, alternative in enumerate(path):

            idv_path = []
            for pair in alternative:
                temp1, temp2 = pairs[pair]
                idv_path.append(temp1)
                idv_path.append(temp2)
            if direction == 'up':
                idv_path = sorted(idv_path, key=lambda x: float(x['absPos']))
            else:
                idv_path = sorted(idv_path, key=lambda x: float(x['absPos']), reverse=True)
            values.append(idv_path)
        result.append(values)
    
    # Sort the order of alternatives based on their % of running direction same as track direction
    sorted_result = []
    for index, route in enumerate(result):
        route_dir = start_n_end_dir[index]
        dir_paprm_arr = []
        for alternative in route:
            up_count = 0
            down_count = 0
            #print(alternative)
            for node in alternative:
                #print(node)
                if tracks_data[node['Y']]['Direction'] == "up":
                    up_count = up_count + 1
                elif tracks_data[node['Y']]['Direction'] == "down":
                    down_count = down_count + 1
                elif tracks_data[node['Y']]['Direction'] == "none":
                    up_count = up_count + 1
                    down_count = down_count + 1
                else:
                    print("Warning, direction error! /43")
            if up_count + down_count != len(alternative):
                print("warning, count error! /45")    
            direction_param = up_count/(up_count + down_count)
            dir_paprm_arr.append(direction_param)
        if route_dir == 'up':
            sorted_dir_param_arr = sorted(enumerate(dir_paprm_arr), key=lambda x: x[1], reverse=True)
        elif route_dir == 'down':
            sorted_dir_param_arr = sorted(enumerate(dir_paprm_arr), key=lambda x: x[1], reverse=False)
        #print(sorted_dir_param_arr, dir_paprm_arr, route_dir)
        sorted_alt = []
        sorted_alt = [route[index] for index, _ in sorted_dir_param_arr]
        sorted_result.append(sorted_alt)
    sorted_result = [[[item['id'] for item in sub_list] for sub_list in inner_list] for inner_list in sorted_result]

    return sorted_result

'''
# Example test
tracks_info = railml_parser.parser('Katrineholm.railml.xml')
[track_data, connection_data, circuitBorder_data] = data_formatting.data_formatting(tracks_info)
pairs = segment_generator.pairing(connection_data, circuitBorder_data)
[start_n_end, up_graph, down_graph, start_n_end_dir] = route_generator_prep.generator_prep(track_data, pairs)
paths = route_generator.generator(start_n_end, start_n_end_dir, up_graph, down_graph)
result = file_generator_prep(paths, pairs, start_n_end_dir, track_data)

print(result)
print(len(result))
for i in range(0,len(result)):
    print(f"    {len(result[i])}")
    for j in range(0,len(result[i])):
        print(f"        {len(result[i][j])}")
'''