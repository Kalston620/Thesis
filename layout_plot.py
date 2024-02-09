import matplotlib.pyplot as plt
import railml_parser

def plot_track_layout(tracks_info):
    # New Figuer
    plt.figure(figsize=(10, 6))

    # Plot each track layout
    for track_name, track_info in tracks_info.items():
        pos_start = track_info['pos_start']
        pos_end = track_info['pos_end']
        y_axis = track_info['track_id']
        # Track
        plt.plot([pos_start, pos_end], [y_axis, y_axis], label=f'Track {track_name}', linestyle='-', color='black')
        # Signal
        for signal in track_info['signals']:
            plt.scatter(pos_start + signal['pos'], y_axis, marker='s', color='red', label=f"{signal['name']} ({track_name})")

        # Switch
        for switch in track_info['switches']:
            plt.scatter(pos_start + switch['pos'], y_axis, marker='^', color='blue', label=f"{switch['name']} ({track_name})")
            #TODO: plot connection for switch
            #for connection in switch['connection']:
            #    plt.plot([pos_start + switch['pos'],])
            
        # Detector
        for detector in track_info['detectors']:
            plt.scatter(pos_start + detector['pos'], y_axis, marker='o', color='green', label=f"{detector['name']} ({track_name})")

    # Add label and title
    plt.xlabel('Position')
    plt.ylabel('Track Layout')
    plt.title('Rail Track Layout')
    plt.legend()
    plt.grid(True)

    # Show plot
    plt.show()

# Test with parser output
file_path = 'example-twotrack.railml.xml'
tracks_info = railml_parser.parser(file_path)

plot_track_layout(tracks_info)
