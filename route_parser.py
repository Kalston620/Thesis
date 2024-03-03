import xml.etree.ElementTree as ET

def parser(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    routes = []

    for route_element in root.findall('route'):
        route = {'id': route_element.get('id'),
                 'name': route_element.get('name'),
                 'start': route_element.get('start'),
                 'end': route_element.get('end')}
        
        alternatives = []
        for alternative_element in route_element.findall('alternative'):
            alternative = {'id': alternative_element.get('id'),
                           'platform': alternative_element.get('platform').lower() == 'true',
                           'nodes': [node_element.get('id') for node_element in alternative_element.findall('node')]}
            alternatives.append(alternative)

        route['alternatives'] = alternatives
        routes.append(route)

    return routes


# Example usage
file_path = 'Katrineholm_Route.xml'
routes = parser(file_path)

# Print the parsed data
for route in routes:
    print(f"Route ID: {route['id']}, Name: {route['name']}, Start: {route['start']}, End: {route['end']}")
    for alternative in route['alternatives']:
        print(f"  Alternative ID: {alternative['id']}, Platform: {alternative['platform']}, Nodes: {alternative['nodes']}")
print(routes)