import matplotlib.pyplot as plt
import railml_parser

def plot_track_layout(tracks_info):
    # New Figuer
    plt.figure(figsize=(10, 6))

    # Plot each track layout
    i = 0
    for track_name, track_info in tracks_info.items():
        pos_start = track_info['pos_start']
        pos_end = track_info['pos_end']

        # Track
        plt.plot([pos_start, pos_end], [i, i], label=f'Track {track_name}', linestyle='-', color='black')

        # Signal
        for signal in track_info['signals']:
            plt.scatter(pos_start + signal['pos'], i, marker='s', color='red', label=f"{signal['name']} ({track_name})")

        # Switch
        for switch in track_info['switches']:
            plt.scatter(pos_start + switch['pos'], i, marker='^', color='blue', label=f"{switch['name']} ({track_name})")

        # Detector
        for detector in track_info['detectors']:
            plt.scatter(pos_start + detector['pos'], i, marker='o', color='green', label=f"{detector['name']} ({track_name})")

        i = i+1
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
