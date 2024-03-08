import railml_parser

def data_formatting(tracks_info):
    # Orgnazning track data and check if the track has open end and check if there is platform
    track_data = []
    connection_data = []
    circuitBorder_data = []
    for track_name, track_info in tracks_info.items():
        main_dir = track_info['mainDir']
        track_id = track_info['track_id']

        if track_info['open_end_begin']:
            open_end_begin = True
            open_end_begin_name = track_info['open_end_begin']
        else:
            open_end_begin = False
            open_end_begin_name = None
        if track_info['open_end_end']:
            open_end_end = True
            open_end_end_name = track_info['open_end_end']
        else: 
            open_end_end = False
            open_end_end_name = None

        if track_info['platform']:
            platform = True
        else:  
            platform = False
        track_data.append({'name': track_name, 'Y': track_id, 'Direction': main_dir,  'Position Start': float(track_info['pos_start']), 'Position End': float(track_info['pos_end']), 'entry_from_start': open_end_begin, 'entry_from_start_name': open_end_begin_name, 'entry_from_end': open_end_end, 'entry_from_end_name': open_end_end_name, 'is_platform': platform})
    
        # Collect connection data
        for connections in track_info['connection_track']:
            connection_data.append(connections)
        for switch in track_info['switches']:
            X = float(switch['absPos'])
            Y = track_id
            for connection in switch['connection']:
                start_id = connection['start_id']
                end_id = connection['end_id']
            connection_data.append({'id': start_id, 'ref': end_id, 'Y_axis': Y, 'X_axis': X})

        # Collect track circuit border
        for circuitBorder in track_info['circuits']:
            circuit_id = circuitBorder['id']
            circuit_absPos = circuitBorder['absPos']
            circuit_dir = circuitBorder['dir']
            circuit_insulatedRail = circuitBorder['insulatedRail']
            circuitBorder_data.append({'id': circuit_id, 'Y': track_id, 'absPos': circuit_absPos, 'dir': circuit_dir, 'insulatedRail': circuit_insulatedRail})
    return track_data, connection_data, circuitBorder_data

'''
# Example test
tracks_info = railml_parser.parser('Katrineholm.railml.xml')
[track_data, connection_data, circuitBorder_data] = data_formatting(tracks_info)
print(track_data)
print(connection_data)
print(circuitBorder_data, len(circuitBorder_data))
'''