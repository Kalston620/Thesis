# Thesis Code
## Work Till 8/2-24:
railml_parser.py will read RailML XML file and extract track name, start and end position (only use 'absPos' in XML file), signal name and position, switches name and position, train detectors name and position. All info will stored in 'tracks_info' with an additional 'track_id', which used as y-axis for plotting.

layout_plot.py will read 'tracks_info and then plot all elements. 
## Update 12/2-24:
Now layout_plot.py can plot switch connections as well, but the shape of the connection depending on the position of switch and start point of the target track. In the example for testing, all switch connection are in 90° angle.
### Examples:
Result with example-split.railml:
![img_folder/split.png](https://github.com/Kalston620/Thesis/blob/cf8332f2aacd34dde478fff6fb7682d3b8f49cbe/img_folder/split.png)

Result with example-twotrack.railml:
![img_folder/twotrack.png](https://github.com/Kalston620/Thesis/blob/a4258dd55f0ed720424fc3640336c925e0761d8f/img_folder/twotrack.png)

Result with Katrineholm.railml.xml:
![img_floder/Katrineholm.png](https://github.com/Kalston620/Thesis/blob/4a4270e89e17f78d2fe3d3d2c40bc894165d4f96/img_folder/Katrineholm.png)