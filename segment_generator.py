from numpy import diff
import railml_parser
import data_formatting

def pairing(connection_data, circuitBorder_data):
    # devide into different group with Y, same track same group
    grouped_circuitBorder_data = {}
    for item in circuitBorder_data:
        Y = item['Y']
        if Y not in grouped_circuitBorder_data:
            grouped_circuitBorder_data[Y] = []

        grouped_circuitBorder_data[Y].append(item)
    #print(grouped_circuitBorder_data)
    pairs = []
    used = []
    for Y, group in grouped_circuitBorder_data.items():
        # Sort group based on absPos
        sorted_group = sorted(group, key=lambda x: float(x['absPos']))
        # Finding pairs, but only on same track
        for i in range(0, len(sorted_group)-1):
            if sorted_group[i]['dir'] == 'up' and sorted_group[i]['insulatedRail'] == 'none':
                for j in range(i+1, len(sorted_group)):
                    if i != j:
                        if sorted_group[j]['dir'] == 'down' and sorted_group[j]['insulatedRail'] == 'none' and float(sorted_group[i]['absPos']) < float(sorted_group[j]['absPos']):
                            pairs.append((sorted_group[i], sorted_group[j]))
                            used.append(sorted_group[i])
                            used.append(sorted_group[j])
                            break
    # Find pairs cross track
    used_set = set(tuple(item.items()) for item in used)
    circuitBorder_data_set = set(tuple(item.items()) for item in circuitBorder_data)
    difference_circuitBorder_data = [dict(item) for item in (circuitBorder_data_set - used_set)]
    for diff_item in difference_circuitBorder_data:
        if diff_item['dir'] == 'up':
            for conn_item in connection_data:
                if diff_item['Y'] == conn_item['Y_axis'] and float(diff_item['absPos']) == conn_item['X_axis']:
                    for other_conn_item in connection_data:
                        if other_conn_item['id'] == conn_item['ref']:
                            for other_diff_item in difference_circuitBorder_data:
                                if other_diff_item['Y'] == other_conn_item['Y_axis'] and float(other_diff_item['absPos']) == other_conn_item['X_axis']:
                                    pairs.append((diff_item, other_diff_item))
                                    used.append(diff_item)
                                    used.append(other_diff_item)
    return pairs

'''
# Example test
tracks_info = railml_parser.parser('Katrineholm.railml.xml')
[track_data, connection_data, circuitBorder_data] = data_formatting.data_formatting(tracks_info)
pairs = pairing(connection_data, circuitBorder_data)
for i in range(25,len(pairs)):
    print(pairs[i])
'''