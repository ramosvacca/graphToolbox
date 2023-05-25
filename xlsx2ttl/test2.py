import pylightxl as xl
from re import sub
import urllib.parse
import yaml


# Defines camel case function
def camel_case(s):
  s = sub(r"(_|-|^[0-9]|\.|\xa0|:|\?)+", " ", s).title().replace(" ", "")
  return ''.join([s[0].lower(), s[1:]])
# defines pascal case function
def pascal_case(s):
  s = sub(r"(_|-|^[0-9]|\.|\xa0)+", " ", s).title().replace(" ", "")
  return s
def clean_case(string):
    return sub(r"(^[0-9]\.?\s?|\.|:|\xa0)+", "", string)
def get_cell_value(sheet_name, cell_address):
    return db.ws(ws=sheet_name).range(address=cell_address)[0][0]

def get_cell_address_string(sheetName, cellAdress):
    return f'{camel_case(sheetName)}_{cellAdress}'
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


#global baseUri, baseUriAbbreviation
baseUri = "<https://sustainable-energy.com/"
baseUriAbbreviation = "sf"

# readxl returns a pylightxl database that holds all worksheets and its data
db = xl.readxl(fn=r"C:\Users\Administrator\Downloads\sust-taxo.xlsx")

# return all sheet names
print(db.ws(ws='Mitigation summary').address(address='A1'))

# for row in db.ws(ws=db.ws_names[0]).rows:
#     print(row)

class Rdfclass:
    def __init__(self, value):
        self.uri = self.makeUri(value)
        self.label = f'{clean_case(value)}'

    def makeUri(self, value):
        return f'{baseUriAbbreviation}:{pascal_case(value)}'

    def get_ttl(self):
        return f'{self.uri} rdf:type rdfs:Class ;\nrdfs:label "{self.label}" .\n'

class Property:

    def __init__(self, prop_type, value, domain=None, range=None, property_prefix="", uri_prefix="", classes_input_dict=None):
        # Type definition
        self.prop_type = prop_type
        self.uri_prefix = uri_prefix

        if prop_type == 1:
            self.type = "owl:ObjectProperty"
        elif prop_type == 2:
            self.type = "owl:DatatypeProperty"
        elif prop_type == 3:
            self.type = "owl:AnnotationProperty"

        # Label definition
        if type(value) == list:
            name = get_cell_value(value[0], value[1])
        else:
            name = value

        if property_prefix == "":
            self.label = clean_case(name)
        else:
            self.label = f'{property_prefix} {clean_case(name)}'

        # Name definition
        if uri_prefix == "":
            # Encodes URI with urllib
            self.uri = f'{baseUriAbbreviation}:{urllib.parse.quote(camel_case(self.label))}'
        else:
            self.uri = f'{uri_prefix}:{camel_case(self.label)}'

        self.domain = classes_output_dict[f'{camel_case(domain[0])}_{domain[1]}'].uri

        try:
            if range.startswith('xsd') == True:
                self.range = range
        except:
            self.range = classes_input_dict[f'{camel_case(range[0])}_{range[1]}'].uri

    def get_ttl(self):
        # Defines the relation (not domain and range) for types 1, 2 and 3
        ttl = ''
        ttl_relation = f'{self.domain} {self.uri} {self.range} .\n'
        # If it is to use the ontology prefix, it adds the type definition and its label
        # otherwise, it is assumed that another ontology shall be imported.
        if self.uri_prefix == "":
            ttl = f'{self.uri} rdf:type {self.type} ;\n' \
                  f'rdfs:label "{self.label}"'
            # If the property is not annotation property (3), it creates domain and range to add to the ttl
            if self.prop_type != 3:
                domain_range_ttl = f';\nrdfs:domain {self.domain} ;\n' \
                                   f'rdfs:range {self.range} .\n'
                return ttl + domain_range_ttl# + ttl_relation
            # else, if it is an Annotation Property, it returns the definition for annotation property and the relation
            else:
                return f'{ttl} .\n' + ttl_relation
        # If the prefix is from another ontology
        else:
            if self.prop_type != 3:
                domain_range_ttl = f'{self.uri} rdfs:domain {self.domain} ;\n' \
                                   f'rdfs:range {self.range} .\n'
                return domain_range_ttl# + ttl_relation
            # else returns the definition for annotation property
            else:
                return ttl_relation

# CLASSES, SUBCLASSES AND PROPERTIES DICTIONARIES

classes = [{'sheet_name': 'Mitigation summary', 'cell': 'A1'},
           {'sheet_name': 'Mitigation summary', 'cell': 'A2'},
           {'sheet_name': 'Mitigation summary', 'cell': 'B2'},
           {'sheet_name': 'Mitigation summary', 'cell': 'C1'},
           {'sheet_name': 'Mitigation summary', 'cell': 'C2'},
           {'sheet_name': 'Mitigation summary', 'cell': 'G2'},
           {'sheet_name': 'Mitigation summary', 'cell': 'H2'},
           {'sheet_name': 'Mitigation summary', 'cell': 'I2'},
           {'sheet_name': 'Mitigation summary', 'cell': 'J2'},
           {'sheet_name': 'Mitigation summary', 'cell': 'K2'},
           {'sheet_name': 'Mitigation full data', 'cell': 'E2'},
           {'sheet_name': 'Mitigation full data', 'cell': 'G1'},
           {'sheet_name': 'Mitigation full data', 'cell': 'J1'},
           {'sheet_name': 'Adaptation summary', 'cell': 'C1'},
           {'sheet_name': 'Adaptation full data', 'cell': 'E2'},
           {'sheet_name': 'Adaptation full data', 'cell': 'G1'},
           {'sheet_name': 'Adaptation full data', 'cell': 'H1'},
           {'sheet_name': 'Adaptation screening criteria', 'cell': 'B1'},
           {'sheet_name': 'Adaptation screening criteria', 'cell': 'B4'},
           {'sheet_name': 'Adaptation screening criteria', 'cell': 'B19'},
           {'sheet_name': 'Regulation', 'cell': 'A1'},
           {'sheet_name': 'BICS', 'cell': 'A1'},
           {'sheet_name': 'TRBC', 'cell': 'A1'}]

subclasses = [{'subclass_sheet_name': 'Mitigation summary', 'subclass': 'C2', 'class_sheet_name': 'Mitigation summary', 'class': 'C1'},
{'subclass_sheet_name': 'Mitigation summary', 'subclass': 'G2', 'class_sheet_name': 'Mitigation summary', 'class': 'C1'},
{'subclass_sheet_name': 'Mitigation summary', 'subclass': 'H2', 'class_sheet_name': 'Mitigation summary', 'class': 'C1'},
{'subclass_sheet_name': 'Mitigation summary', 'subclass': 'I2', 'class_sheet_name': 'Mitigation summary', 'class': 'C1'},
{'subclass_sheet_name': 'Mitigation summary', 'subclass': 'J2', 'class_sheet_name': 'Mitigation summary', 'class': 'C1'},
{'subclass_sheet_name': 'Mitigation summary', 'subclass': 'K2', 'class_sheet_name': 'Mitigation summary', 'class': 'C1'},
{'subclass_sheet_name': 'Adaptation screening criteria', 'subclass': 'B4', 'class_sheet_name': 'Adaptation screening criteria', 'class': 'B1'},
{'subclass_sheet_name': 'Adaptation screening criteria', 'subclass': 'B19', 'class_sheet_name': 'Adaptation screening criteria', 'class': 'B1'}]

object_properties = [
# Activity environmentalContributions
{
        'type': 1,
        'name': ['Mitigation summary', 'C1'],
        'domain': ['Mitigation summary', 'B2'],
        'range': ['Mitigation summary', 'C1'],
        'property_prefix': 'has',
        'uri_prefix': ''
    },
# Activity has bics mapping
{
        'type': 1,
        'name': ['BICS', 'A1'],
        'domain': ['Mitigation summary', 'B2'],
        'range': ['BICS', 'A1'],
        'property_prefix': 'has',
        'uri_prefix': ''
    },
# Activity has trbc mapping
{
        'type': 1,
        'name':['TRBC', 'A1'],
        'domain': ['Mitigation summary', 'B2'],
        'range': ['TRBC', 'A1'],
        'property_prefix': 'has',
        'uri_prefix': ''
    },
#activity is part of NaceMacroSector
{
        'type': 3,
        'name': 'is part of',
        'domain': ['Mitigation summary', 'B2'],
        'range': ['Mitigation summary', 'A2'],
        'uri_prefix': 'dc',
        'property_prefix': ''
    },
#ClimateChangeMitigation isEnabling Boolean
{
        'type': 2,
        'name': ['Mitigation summary', 'E3'],
        'domain': ['Mitigation summary', 'C2'],
        'range': 'xsd:boolean',
        'uri_prefix': '',
        'property_prefix': 'is'
    },
#ClimateChangeMitigation basedOnOwnPerformance Boolean
{
        'type': 2,
        'name': ['Mitigation summary', 'D3'],
        'domain': ['Mitigation summary', 'C2'],
        'range': 'xsd:boolean',
        'uri_prefix': '',
        'property_prefix': 'based on'
    },
#EnvironmentalContributions hasTypeOfContribution String
{
        'type': 2,
        'name': ['Mitigation summary', 'C3'],
        'domain': ['Mitigation summary', 'C1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': 'has'
    },
#ClimateChangeMitigation isTransitionActivity Boolean
{
        'type': 2,
        'name': ['Mitigation summary', 'F3'],
        'domain': ['Mitigation summary', 'C2'],
        'range': 'xsd:boolean',
        'uri_prefix': '',
        'property_prefix': 'is'
    },
# Activity level2 string
{
        'type': 2,
        'name': ['Mitigation full data', 'B2'],
        'domain': ['Mitigation summary', 'B2'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': ''
    },
# Activity level3 string
{
        'type': 2,
        'name': ['Mitigation full data', 'C2'],
        'domain': ['Mitigation summary', 'B2'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': ''
    },
# Activity level4 string
{
        'type': 2,
        'name': ['Mitigation full data', 'D2'],
        'domain': ['Mitigation summary', 'B2'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': ''
    },
# Activity description
{
        'type': 3,
        'name': 'description',
        'domain': ['Mitigation summary', 'B2'],
        'range': 'xsd:string',
        'uri_prefix': 'dc',
        'property_prefix': ''
    },
# Mitigation Criteria hasPrinciple string
{
        'type': 2,
        'name': ['Mitigation full data', 'G2'],
        'domain': ['Mitigation full data', 'G1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': 'has'
    },
# Mitigation Criteria hasMetric&Threshold string
{
        'type': 2,
        'name': ['Mitigation full data', 'H2'],
        'domain': ['Mitigation full data', 'G1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': 'has'
    },
# Mitigation Criteria hasRationale string
{
        'type': 2,
        'name': ['Mitigation full data', 'I2'],
        'domain': ['Mitigation full data', 'G1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': 'has'
    },
# Activity has DNSHassessment
{
        'type': 1,
        'name': ['Mitigation full data', 'J1'],
        'domain': ['Mitigation full data', 'E2'],
        'range': ['Mitigation full data', 'J1'],
        'uri_prefix': '',
        'property_prefix': 'has'
    },
# DNSH assessment Summary string
{
        'type': 3,
        'name': ['Mitigation full data', 'J2'],
        'domain': ['Mitigation full data', 'J1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': ''
    },
# DNSH assessment Adaptation string
{
        'type': 2,
        'name': ['Mitigation full data', 'K2'],
        'domain': ['Mitigation full data', 'J1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': ''
    },
# DNSH assessment Water string
{
        'type': 2,
        'name': ['Mitigation full data', 'L2'],
        'domain': ['Mitigation full data', 'J1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': 'dnsh on'
    },
# DNSH assessment Water based on legislation boolean
{
        'type': 2,
        'name': ['Mitigation full data', 'M2'],
        'domain': ['Mitigation full data', 'J1'],
        'range': 'xsd:boolean',
        'uri_prefix': '',
        'property_prefix': ''
    },
# DNSH assessment WaterRelevantRegulation string
{
        'type': 2,
        'name': ['Mitigation full data', 'N2'],
        'domain': ['Mitigation full data', 'J1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': ''
    },
# DNSH assessment Circular Economy string
{
        'type': 2,
        'name': ['Mitigation full data', 'O2'],
        'domain': ['Mitigation full data', 'J1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': 'dnsh on'
    },
# DNSH assessment circular economy based on legislation boolean
{
        'type': 2,
        'name': ['Mitigation full data', 'P2'],
        'domain': ['Mitigation full data', 'J1'],
        'range': 'xsd:boolean',
        'uri_prefix': '',
        'property_prefix': ''
    },
# DNSH assessment circular economyRelevantRegulation string
{
        'type': 2,
        'name': ['Mitigation full data', 'Q2'],
        'domain': ['Mitigation full data', 'J1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': ''
    },
# DNSH assessment pollution string
{
        'type': 2,
        'name': ['Mitigation full data', 'R2'],
        'domain': ['Mitigation full data', 'J1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': 'dnsh on'
    },
# DNSH assessment pollution based on legislation boolean
{
        'type': 2,
        'name': ['Mitigation full data', 'S2'],
        'domain': ['Mitigation full data', 'J1'],
        'range': 'xsd:boolean',
        'uri_prefix': '',
        'property_prefix': ''
    },
# DNSH assessment pollutionRelevantRegulation string
{
        'type': 2,
        'name': ['Mitigation full data', 'T2'],
        'domain': ['Mitigation full data', 'J1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': ''
    },
# DNSH assessment ecosystems string
{
        'type': 2,
        'name': ['Mitigation full data', 'U2'],
        'domain': ['Mitigation full data', 'J1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': 'dnsh on'
    },
# DNSH assessment ecosystems based on legislation boolean
{
        'type': 2,
        'name': ['Mitigation full data', 'V2'],
        'domain': ['Mitigation full data', 'J1'],
        'range': 'xsd:boolean',
        'uri_prefix': '',
        'property_prefix': ''
    },
# DNSH assessment ecosystemsRelevantRegulation string
{
        'type': 2,
        'name': ['Mitigation full data', 'W2'],
        'domain': ['Mitigation full data', 'J1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': ''
    },
# aCTIVITY has adaptation criteria
{
        'type': 1,
        'name': ['Adaptation full data', 'G1'],
        'domain': ['Adaptation full data', 'E2'],
        'range': ['Adaptation full data', 'G1'],
        'uri_prefix': '',
        'property_prefix': 'has'
    },
# Adaptation criteria has technical screening criteria string
{
        'type': 2,
        'name': ['Adaptation full data', 'G2'],
        'domain': ['Adaptation full data', 'G1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': 'has'
    },
# DNSH has mitigation information
{
        'type': 2,
        'name': ['Adaptation full data', 'I2'],
        'domain': ['Adaptation full data', 'H1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix': 'has'
    },
# Adaotation screening criteria explanatio
{
        'type': 3,
        'name': ['Adaptation screening criteria', 'B2'],
        'domain': ['Adaptation screening criteria', 'B1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix':''
    },
# adaptation dc:description
{
        'type': 3,
        'name': 'description',
        'domain': ['Adaptation screening criteria', 'B1'],
        'range': 'xsd:string',
        'uri_prefix': 'dc',
        'property_prefix':''
    },
# Regulation and directive title
{
        'type': 3,
        'name': 'title',
        'domain': ['Regulation', 'A1'],
        'range': 'xsd:string',
        'uri_prefix': 'dc',
        'property_prefix':''
    },
# Regulation and directive comissionWebsite
{
        'type': 2,
        'name': ['Regulation', 'C3'],
        'domain': ['Regulation', 'A1'],
        'range': 'xsd:anyURI',
        'uri_prefix': '',
        'property_prefix':''
    },
# Regulation and directive link
{
        'type': 2,
        'name': ['Regulation', 'E3'],
        'domain': ['Regulation', 'A1'],
        'range': 'xsd:anyURI',
        'uri_prefix': '',
        'property_prefix':''
    },
# BICS mapping has bics code
{
        'type': 2,
        'name': ['BICS', 'A2'],
        'domain': ['BICS', 'A1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix':''
    },
# BICS mapping has bics name
{
        'type': 2,
        'name': ['BICS', 'C2'],
        'domain': ['BICS', 'A1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix':''
    },
# level
{
        'type': 3,
        'name': ['BICS', 'B2'],
        'domain': ['BICS', 'A1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix':''
    },
# TRBC mapping has bics NACE class
{
        'type': 2,
        'name': ['TRBC', 'C2'],
        'domain': ['TRBC', 'A1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix':''
    },
# TRBC mapping has bics NACE class
{
        'type': 2,
        'name': ['TRBC', 'D2'],
        'domain': ['TRBC', 'A1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix':''
    },
# TRBC mapping has TRBC level
{
        'type': 2,
        'name': ['TRBC', 'E2'],
        'domain': ['TRBC', 'A1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix':''
    },
# TRBC mapping has TRBC code
{
        'type': 2,
        'name': ['TRBC', 'F2'],
        'domain': ['TRBC', 'A1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix':''
    },
# TRBC mapping has TRBC description
{
        'type': 2,
        'name': ['TRBC', 'G2'],
        'domain': ['TRBC', 'A1'],
        'range': 'xsd:string',
        'uri_prefix': '',
        'property_prefix':''
    },
]


# RDF CLASSES ##
def create_rdf_classes(input_list):
    output_dict = {}
    """This function creates RDF classes from a list of dictionaries.

    Args:
        classes (list of dict): A list of dictionaries, where each dictionary represents a class.

    Returns:
        dict: A dictionary, where the keys are the class names and the values are the RDF classes.
    """

    # Iterate over the classes.
    for class_dict in input_list:

        # Get the current class value.
        current_class_value = get_cell_value(class_dict["sheet_name"], class_dict["cell"])

        cell_address_string = get_cell_address_string(class_dict["sheet_name"], class_dict["cell"])

        # Create an RDF class from the current class value.
        output_dict[cell_address_string] = Rdfclass(current_class_value)

    return output_dict


# RDF SUBCLASSES ##
def create_rdf_subclasses(subclasses_input_list, classes_input_dict):
    output_list = []
    """
    Args:
        subclasses (list of dict): A list of dictionaries, where each dictionary represents a subclass.

    Returns:
        list of str: A list of RDF triples.
    """

    # Iterate over the subclasses.
    for subclass_dict in subclasses_input_list:
        # Get the URI of the subclass.
        subclass_uri = classes_input_dict[
            get_cell_address_string(subclass_dict["subclass_sheet_name"], subclass_dict["subclass"])].uri

        # Get the URI of the superclass.
        superclass_uri = classes_input_dict[
            get_cell_address_string(subclass_dict["class_sheet_name"], subclass_dict["class"])].uri

        # Add the RDF triple to the list.
        output_list += [subclass_uri + ' rdfs:subClassOf ' + superclass_uri]

    return output_list


# RDF PROPERTIES ##
def create_properties_list(input_list):
    """This function creates a list of RDF properties from a list of dictionaries.

    Args:
        input_list (list of dict): A list of dictionaries, where each dictionary represents a property.

    Returns:
        list of Property: A list of RDF properties.
    """
    output_list = []
    # Iterate over the object properties.
    for each_property in input_list:

        # Create a Property object.
        property = Property(each_property['type'], each_property['name'], each_property['domain'], each_property['range'], each_property['property_prefix'], each_property['uri_prefix'], classes_output_dict)

        # Add the Property object to the list.
        output_list.append(property)

    return output_list


classes_output_dict = create_rdf_classes(classes)

sub_classes_triples = create_rdf_subclasses(subclasses, classes_output_dict)

properties_list = create_properties_list(object_properties)

# Print the RDF classes, subclasses and properties

for cellAddress, classObject in classes_output_dict.items():
    print(classObject.get_ttl())

for subclass_relation in sub_classes_triples:
    print(subclass_relation + '.\n')

for property_object in properties_list:
    print(property_object.get_ttl())

