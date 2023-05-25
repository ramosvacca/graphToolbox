import pylightxl as xl
from re import sub
import urllib.parse
import yaml
import sys

baseUri = "<https://sustainable-energy.com/"
baseUriAbbreviation = "sf"


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


def make_input_lists(filepath):

    """This function returns a list of classes, a list of subclasses, and a list of properties from a YAML file."""

    # Open the YAML file.
    with open(filepath, 'r') as file:
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

        if property_prefix == "" or property_prefix == None:
            self.label = clean_case(name)
        else:
            self.label = f'{property_prefix} {clean_case(name)}'

        # Name definition
        if uri_prefix == "" or uri_prefix == None:
            # Encodes URI with urllib
            self.uri = f'{baseUriAbbreviation}:{urllib.parse.quote(camel_case(self.label))}'
        else:
            self.uri = f'{uri_prefix}:{camel_case(self.label)}'

        self.domain = classes_input_dict[f'{camel_case(domain[0])}_{domain[1]}'].uri

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
        if self.uri_prefix == "" or self.uri_prefix == None:
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


# RDF CLASSES ##
def create_rdf_classes(classes):
    output_dict = {}
    """This function creates RDF classes from a list of dictionaries.

    Args:
        classes (list of dict): A list of dictionaries, where each dictionary represents a class.

    Returns:
        dict: A dictionary, where the keys are the class names and the values are the RDF classes.
    """

    # Iterate over the classes.
    for class_dict in classes:

        # Get the current class value.
        current_class_value = get_cell_value(class_dict["sheet_name"], class_dict["cell"])

        cell_address_string = get_cell_address_string(class_dict["sheet_name"], class_dict["cell"])

        # Create an RDF class from the current class value.
        output_dict[cell_address_string] = Rdfclass(current_class_value)

    return output_dict


# RDF SUBCLASSES ##
def create_rdf_subclasses(subclasses, classes_input_dict):
    output_list = []
    """
    Args:
        subclasses (list of dict): A list of dictionaries, where each dictionary represents a subclass.

    Returns:
        list of str: A list of RDF triples.
    """

    # Iterate over the subclasses.
    for subclass_dict in subclasses:
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
def create_properties_list(properties, classes_input_dict):
    """This function creates a list of RDF properties from a list of dictionaries.

    Args:
        properties (list of dict): A list of dictionaries, where each dictionary represents a property.

    Returns:
        list of Property: A list of RDF properties.
    """
    output_list = []
    # Iterate over the object properties.
    for each_property in properties:

        # Create a Property object.
        property = Property(each_property['type'], each_property['name'], each_property['domain'], each_property['range'], each_property['property_prefix'], each_property['uri_prefix'], classes_input_dict)

        # Add the Property object to the list.
        output_list.append(property)

    return output_list

def main():
    """This function is the main entry point for the program."""
    # readxl returns a pylightxl database that holds all worksheets and its data
    global db

    # Get the filepath from the command line arguments.
    db_filepath = sys.argv[1]
    yaml_filepath = sys.argv[2]
    # # Read the file and generate RDF triples.
    # db = xl.readxl(fn=r"C:\Users\Administrator\Downloads\example.xlsx")
    db = xl.readxl(fn=db_filepath)
    # CLASSES, SUBCLASSES AND PROPERTIES DICTIONARIES
    # Call the function and print the results.
    # classes, subclasses, properties = make_input_lists('mapping.yaml')
    classes, subclasses, properties = make_input_lists(yaml_filepath)

    classes_output_dict = create_rdf_classes(classes)

    sub_classes_triples = create_rdf_subclasses(subclasses, classes_output_dict)

    properties_list = create_properties_list(properties, classes_output_dict)

    # Print the RDF classes, subclasses and properties
    print("""@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix sf: <http://sustainable-finance.org/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
""")

    for cellAddress, classObject in classes_output_dict.items():
        print(classObject.get_ttl())

    for subclass_relation in sub_classes_triples:
        print(subclass_relation + '.\n')

    for property_object in properties_list:
        print(property_object.get_ttl())

    print("""###  http://purl.org/dc/terms/isPartOf
<http://purl.org/dc/terms/isPartOf> rdf:type owl:AnnotationProperty ;
                                    <http://purl.allotrope.org/ontologies/property#AFX_0002865> <http://purl.org/dc/terms/> ;
                                    rdfs:isDefinedBy <http://purl.allotrope.org/voc/afo/REC/2022/06/curation> ;
                                    rdfs:label "is part of" ;
                                    <http://www.w3.org/2004/02/skos/core#prefLabel> "is part of" ;
                                    rdfs:subPropertyOf <http://purl.org/dc/elements/1.1/relation> ,
                                                       <http://purl.org/dc/terms/relation> .""")

if __name__ == "__main__":
    main()
