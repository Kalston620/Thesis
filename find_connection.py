def find_end_point(connection: dict, connection_track: list):
    # This file will find and return the coordinates of the other end of the switch
    # Input based on the output of the railml_parser, but do not directly use in the program
    start_id_switch = connection['start_id']
    for conn in connection_track:
        if conn['ref'] == start_id_switch:
            X = conn['X_axis']
            Y = conn['Y_axis']
    return X,Y