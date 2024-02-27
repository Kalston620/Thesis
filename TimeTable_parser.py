import xml.etree.ElementTree as ET

def parser(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    lineTraffics = []

    for line_element in root.findall('line'):
        line = {'id': line_element.get('id'),
                'name': line_element.get('name'),
                'start': line_element.get('start'),
                'end': line_element.get('end'),
                'route': line_element.get('route'),
                'timeFronm': line_element.get('timeFrom'),
                'timeTo': line_element.get('timeTo'),
                'freq': line_element.get('freq'),
                'stop': line_element.get('stop'),
                'priority': line_element.get('priority')}
        
        lineTraffics.append(line)
    # Rearrange the order according to priority
    lineTraffics = sorted(lineTraffics, key=lambda x: int(x['priority']))
    return lineTraffics


# Example test
file_path = 'Katrineholm_TimeTable.xml'
lineTraffics = parser(file_path)

for line in lineTraffics:
    print( print(f"Line ID: {line['id']}, Line Name: {line['name']}, Start: {line['start']}, End: {line['end']}, Route: {line['route']}, Time From: {line['timeFronm']}, Time To: {line['timeTo']}, Frequency: {line['freq']}, Stop: {line['stop']}, Priority: {line['priority']}"))

