import yaml


def make_input_lists():

    """This function returns a list of classes, a list of subclasses, and a list of properties from a YAML file."""

    # Open the YAML file.
    with open('mapping.yaml', 'r') as file:
        xlsx_rdf_mapping = yaml.safe_load(file)

    # Get the list of classes.
    classes = []
    for individual in xlsx_rdf_mapping['classes']:
        classes.append(individual)

    # Get the list of subclasses.
    subclasses = []
    for individual in xlsx_rdf_mapping['subclasses']:
        subclasses.append(individual)

    # Get the list of properties.
    properties = []
    for individual in xlsx_rdf_mapping['properties']:
        properties.append(individual)

    # Return the lists.
    return classes, subclasses, properties


# Call the function and print the results.
classes, subclasses, properties = make_input_lists()
#print(classes)
#print(subclasses)
#print(properties)

for i in properties:
    print(i)