def find_end_point(connection: dict, connection_track: list):
    start_id_switch = connection['start_id']
    for conn in connection_track:
        if conn['Start'] == start_id_switch:
            X = conn['X_axis']
            Y = conn['Y_axis']
    return X,Y