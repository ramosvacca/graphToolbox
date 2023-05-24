import yaml

with open('mapping.yaml', 'r') as file:
    prime_service = yaml.safe_load(file)

for each_class in prime_service['classes']:
    print(each_class)

for each_subclass in prime_service['subclasses']:
    print(each_subclass)

for each_property in prime_service['properties']:
    print(each_property)