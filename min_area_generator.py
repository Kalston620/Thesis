import railml_parser
import find_connection
import numpy as np

def generator(tracks_info):
    #print(tracks_info)
    main_line_area = []
    switch_area = []
    # Preperation for switch
    track_connection = []
    for track_name, track_info in tracks_info.items():
        for connection_track in track_info['connection_track']:
            #print(connection_track)
            track_connection.append(connection_track)
        for switches in track_info['switches']:
            for connections in switches['connection']:
                #print(connections)
                #track_connection.append(connections)
                y = track_info['track_id']
                x = switches['pos']
                start = connections['start_id']
                end = connections['end_id']
                temp = {'id': start, 'ref': end, 'Y_axis': y, 'X_axis': x}
                track_connection.append(temp)
    for track_name, track_info in tracks_info.items():
        # Get ID and direction for references
        track_id = track_info['track_id']
        main_dir = track_info['mainDir']
        pos_start = float(track_info['pos_start'])
        pos_end = float(track_info['pos_end'])
        #print(track_id, main_dir)
        # Get all signal direction and position, for generating the minimal maintenance areas
        signals = []
        for signal in track_info['signals']:
            sig_dir = signal['dir']
            sig_pos = signal['pos']
            signals.append([sig_dir, float(sig_pos) + pos_start])
        # Disregard unwanted element (not in same direction)
        if main_dir == 'up':
            signals = [signal for signal in signals if signal[0] != 'down']
            signals = sorted(signals, key=lambda x:x[1])
            #print(signals)
            # New array, add start and end position of track, sort by position
            node_pos = [signal[1] for signal in signals]
            node_pos.insert(0,pos_start)
            node_pos.append(pos_end)
            #print(node_pos)
        elif main_dir == 'down':
            signals = [signal for signal in signals if signal[0] != 'up']
            signals = sorted(signals, key=lambda x:x[1])
            # New array, add start and end position of track, sort by position
            node_pos = [signal[1] for signal in signals]
            node_pos.insert(0,pos_start)
            node_pos.append(pos_end)
        else:
            print("Track Main direction error!")
            break
        #print(node_pos)
        # Pair generate (main line only)
        for i in range(0,len(node_pos)-1):
            start = [track_id, node_pos[i]]
            end = [track_id, node_pos[i+1]]
            main_line_area.append((start, end))
        # Switch pair generate
        for switch in track_info['switches']:
            y1 = track_id
            x1 = pos_start + switch['pos']
            for connection in switch['connection']:
                x2, y2 = find_connection.find_end_point(connection, track_connection)
                switch_area.append(([y1, x1], [y2, x2]))
    # Find connection between main line area
    #print(main_line_area)
    len_main_line = len(main_line_area)
    connection = []
    for i in range(len_main_line):
        conn = []
        y = main_line_area[i][0][0]
        x1 = main_line_area[i][0][1]
        x2 = main_line_area[i][1][1]
        for j in range(len_main_line):
            if i == j:
                continue
            if main_line_area[j][0][0] == y and (main_line_area[j][0][1] == x2 or main_line_area[j][1][1] == x1):
                conn.append(j)
        connection.append(conn)
    #print(connection)
    # Find connection between switch and main line area
    #print(switch_area, len(switch_area))
    # Remove same elements
    for area in switch_area:
        first = area[0]
        second = area[1]
        for other in switch_area:
            if area == other:
                continue
            if other[0] == second and other[1] == first:
                switch_area.remove(area)
    #print(switch_area, len(switch_area))
    # Find connection to main line
    switch_connection = []
    for area in switch_area:
        temp = []
        first = area[0]
        second = area[1]
        for i in range(len(main_line_area)):
            if first[0] == main_line_area[i][0][0] and first[1] >= main_line_area[i][0][1] and first[1] <= main_line_area[i][1][1]:
                temp.append(i)
            elif second[0] == main_line_area[i][0][0] and second[1] >= main_line_area[i][0][1] and second[1] <= main_line_area[i][1][1]:
                temp.append(i)
        switch_connection.append(temp)
    #print(switch_connection)
    # Find if switch cross each other
    switch_cross = []
    for area in switch_area:
        y1, x1 = area[0][0], area[0][1]
        y2, x2 = area[1][0], area[1][1]
        temp = []
        for i in range(0,len(switch_area)):
            other = switch_area[i]
            y3, x3 = other[0][0], other[0][1]
            y4, x4 = other[1][0], other[1][1]
            if area == other:
                continue
            px= ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4)) / ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)) 
            py= ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4)) / ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
            if ((x1<=px<=x2 or x2<=px<=x1) and (y1<=py<=y2 or y2<=py<=y1))and((x3<=px<=x4 or x4<=px<=x3) and (y3<=py<=y4 or y4<=py<=y3)):
                temp.append(i)
        switch_cross.append(temp)
    #print(switch_cross)
    return main_line_area, connection, switch_area, switch_connection, switch_cross

'''
# Example test
file_path = 'Katrineholm.railml.xml'
tracks_info = railml_parser.parser(file_path)
main_line_area, connection, switch_area, switch_connection, switch_cross = generator(tracks_info)
#print(main_line_area, connection, switch_area, switch_connection, switch_cross)
'''