import pylightxl as xl
from re import sub
import urllib.parse

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


#global baseUri, baseUriAbbreviation
baseUri = "<https://sustainable-energy.com/"
baseUriAbbreviation = "sf"

# ENTITIES CONTAINERS ##
classes_dict = {}           # will contain classes as objects referenced by sheet name and cell address
sub_classes_triples = []    # will contain a list of strings - subclasses triples
properties_list = []        # will contain a list of object properties

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

    def __init__(self, prop_type, value, domain=None, range=None, property_prefix="", uri_prefix="", dict=classes_dict):
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

        self.domain = classes_dict[f'{camel_case(domain[0])}_{domain[1]}'].uri

        try:
            if range.startswith('xsd') == True:
                self.range = range
        except:
            self.range = classes_dict[f'{camel_case(range[0])}_{range[1]}'].uri

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

classes = {
    'Mitigation summary': ["A2","B2","C1","C2","G2","H2","I2","J2","K2"],
    'Mitigation full data': ["E2","G1","J1"],
    'Adaptation summary': ["C1"],
    'Adaptation full data': ["E2","G1","H1"],
    'Adaptation screening criteria': ["B1","B4","B19"],
    'Regulation': ["A1"],
    'BICS':["A1"],
    'TRBC':["A1"]
        }

subclasses = {
    'Mitigation summary': [["C2","C1"],["G2","C1"],["H2","C1"],["I2","C1"],["J2","C1"],["K2","C1"]],
    'Mitigation full data': [],
    'Adaptation summary': [],
    'Adaptation full data': [],
    'Adaptation screening criteria': [["B4","B1"],["B19","B1"]],
        }
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

for this_sheet_name, cell_addresses_list in classes.items():
    for cell_address in cell_addresses_list:
        currentClassValue = get_cell_value(this_sheet_name, cell_address)
        classes_dict[f'{camel_case(this_sheet_name)}_{cell_address}'] = Rdfclass(currentClassValue)
        print(classes_dict[f'{camel_case(this_sheet_name)}_{cell_address}'].get_ttl())

# RDF SUBCLASSES ##

# SubClasses definition and serialization as a pair of [SubClass, Class]

for subclass_dict in subclasses:
    sub_classes_triples += [classes_dict[f'{camel_case(subclass_dict["subclass_sheet_name"])}_{subclass_dict["subclass"]}'].uri + ' rdfs:subClassOf ' + classes_dict[f'{camel_case(subclass_dict["class_sheet_name"])}_{subclass_dict["class"]}'].uri]

for subclass_relation in sub_classes_triples:
    print(subclass_relation+'.\n')

# Properties processing
# Object Property → should be a list of dictionaries:
# Each dictionary describes one property and should provide the following arguments:
# type → 1 - Object Property, 2 - Datatype Property, 3 - Annotation Property
# name → the name of the property as a reference list [sheet name, cell reference]
# domain → it should be a reference to a cell or list of references to a cell [sheet name, cell reference]
# range → it should be a reference to a cell or list of references to a cell [sheet name, cell reference]
# propertyPrefix → if the URI is to have a prefix, it should be specified, e.g. has, is, etc.
# uriPrefix → the URI prefix to be used, default ontology baseURI

# RDF PROPERTIES ##

for each_property in object_properties:
    properties_list += [Property(each_property['type'],each_property['name'],each_property['domain'],each_property['range'],each_property['property_prefix'],each_property['uri_prefix'])]

for property_object in properties_list:
    print(property_object.get_ttl())

