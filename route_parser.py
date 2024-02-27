import xml.etree.ElementTree as ET

def parser(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    routes = []

    for route_element in root.findall('route'):
        route = {'id': route_element.get('id'),
                 'name': route_element.get('name'),
                 'start': route_element.get('start'),
                 'end': route_element.get('end'),
                 'alternatives': []}

        for alt_elem in route_element.findall('alternative'):
            alternative = {'id': alt_elem.get('id'),
                           'platform': alt_elem.get('platform'),
                           'nodes': [node.get('id') for node in alt_elem.findall('node')]}
            route['alternatives'].append(alternative)

        routes.append(route)

    return routes

'''
# Example test:
file_path = 'Katrineholm_Route.xml'
routes = parser(file_path)

# Print output
for route in routes:
    print(f"Route {route['id']}: {route['name']} ({route['start']} to {route['end']})")
    for alt in route['alternatives']:
        print(f"  Alternative {alt['id']}: Platform {alt['platform']}, Nodes {alt['nodes']}")
'''