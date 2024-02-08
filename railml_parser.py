import xml.etree.ElementTree as ET

def parser(file_path):
    # Step 1: Parse the RailML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Step 2: Define the RailML namespace
    namespace = {'railml': 'http://www.railml.org/schemas/2013'}

    # Step 3: Define a dictionary to store information about tracks
    tracks_info = {}

    # Step 4: Extract and store information about tracks, signals, switches, and detectors
    i = 0
    for track_element in root.findall('.//railml:track', namespace):
        # Extract track information
        track_id = i
        track_name = track_element.get('name', '')
        pos_start = float(track_element.find('.//railml:trackBegin', namespace).get('absPos', '0.0'))
        pos_end = float(track_element.find('.//railml:trackEnd', namespace).get('absPos', '0.0'))

        # Extract signals for the track
        signals = []
        for signal_element in track_element.findall('.//railml:ocsElements/railml:signals/railml:signal', namespace):
            signal_name = signal_element.get('name', '')
            signal_pos = float(signal_element.get('pos', '0.0'))
            signals.append({'name': signal_name, 'pos': signal_pos})

        # Extract switches for the track
        switches = []
        for switch_element in track_element.findall('.//railml:trackTopology/railml:connections/railml:switch', namespace):
            switch_name = switch_element.get('id', '')
            switch_pos = float(switch_element.get('pos', '0.0'))
            switches.append({'name': switch_name, 'pos': switch_pos})

        # Extract detectors for the track
        detectors = []
        for detector_element in track_element.findall('.//railml:ocsElements/railml:trainDetectionElements/railml:trainDetector', namespace):
            detector_name = detector_element.get('name', '')
            detector_pos = float(detector_element.get('pos', '0.0'))
            detectors.append({'name': detector_name, 'pos': detector_pos})

        # Store track information in the dictionary
        tracks_info[track_name] = {
            'track_id' : track_id,
            'pos_start': pos_start,
            'pos_end': pos_end,
            'signals': signals,
            'switches': switches,
            'detectors': detectors
        }

        i = i+1

    # Return the extracted details
    return tracks_info
'''
# Example test:
file_path = 'example-split.railml.xml'
tracks_info = parser(file_path)

# Print extracted details
for track_name, track_info in tracks_info.items():
    print(f"\nTrack: {track_name}, Track ID: {track_info['track_id']}, Position Start: {track_info['pos_start']}, Position End: {track_info['pos_end']}")
    print("Signals:")
    for signal in track_info['signals']:
        print(f"  Signal Name: {signal['name']}, Position: {signal['pos']}")
    print("Switches:")
    for switch in track_info['switches']:
        print(f"  Switch Name: {switch['name']}, Position: {switch['pos']}")
    print("Detectors:")
    for detector in track_info['detectors']:
        print(f"  Detector Name: {detector['name']}, Position: {detector['pos']}")
'''