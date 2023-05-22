import pylightxl as xl
from re import sub

# Defines camel case function
def camel_case(s):
  s = sub(r"(_|-|^[0-9]|\.|\xa0)+", " ", s).title().replace(" ", "")
  return ''.join([s[0].lower(), s[1:]])
# defines pascal case function
def pascal_case(s):
  s = sub(r"(_|-|^[0-9]|\.|\xa0)+", " ", s).title().replace(" ", "")
  return s


global baseUri, baseUriAbbreviation
baseUri = "<https://sustainable-energy.com/"
baseUriAbbreviation = "sf"
classesDict = {}
subClassesTriples = []

# readxl returns a pylightxl database that holds all worksheets and its data
db = xl.readxl(fn=r"C:\Users\Administrator\Downloads\sust-taxo.xlsx")

# return all sheetnames
print(db.ws(ws='Mitigation summary').address(address='A1'))

# for row in db.ws(ws=db.ws_names[0]).rows:
#     print(row)

class Rdfclass:
    def __init__(self, value):
        self.uri = self.makeUri(value)
        self.label = f'{self.uri} rdfs:label {value} .'

    def makeUri(self, value):
        return f'{baseUriAbbreviation}:{pascal_case(value)}'


class Property:

    def __init__(self, prop_type, name, domain, range, property_prefix="", uri_prefix="", dict=classesDict):
        # Type definition
        if prop_type == 1:
            self.type = "owl:ObjectProperty"
        elif prop_type == 2:
            self.type = "owl:DatatypeProperty"
        elif prop_type == 3:
            self.type = "owl:AnnotationProperty"

        # Label definition
        if property_prefix == "":
            self.label = name
        else:
            self.label = f'{property_prefix} {name}'

        # Name definition
        if uri_prefix == "":
            self.name = f'{baseUriAbbreviation}:{camel_case(self.label)}'
        else:
            self.name = f'{uri_prefix}:{camel_case(self.label)}'

        self.domain = domain
        self.range = range



# Classes definition and serialization
# its input is a dictionary with the sheet names as keys and lists of cell addreses as values
classes = {
    'Mitigation summary': ["A2","B2","C1","C2","G2","H2","I2","J2","K2"],
    'Mitigation full data': ["B2","C2","D2"],
    'Adaptation summary': ["C1"]
        }

for sheet_name, cell_addresses_list in classes.items():
    for cell_address in cell_addresses_list:
        currentClassValue = db.ws(ws=sheet_name).range(address=cell_address)[0][0]
        classesDict[f'{camel_case(sheet_name)}_{cell_address}'] = Rdfclass(currentClassValue)
        print(classesDict[f'{camel_case(sheet_name)}_{cell_address}'].uri)

# for key, value in classesDict.items():
#     print(value.uri)

# SubClasses definition and serialization as a pair of [SubClass, Class]

# subclasses = [["C2","C1"],["G2","C1"],["H2","C1"],["I2","C1"],["J2","C1"],["K2","C1"]]
# for SubClass, Class in subclasses:
#     subClassesTriples += [f'{classesDict[SubClass].uri} rdfs:subClassOf {classesDict[Class].uri}']

# Properties processing
# Object Property → should be a list of dictionaries:
# Each dictionary describes one property and should provide the following arguments:
# type → 1 - Object Property, 2 - Datatype Property, 3 - Annotation Property
# name → the name of the property as a reference list [sheet name, cell reference]
# domain → it should be a reference to a cell or list of references to a cell [sheet name, cell reference]
# range → it should be a reference to a cell or list of references to a cell [sheet name, cell reference]
# propertyPrefix → if the URI is to have a prefix, it should be specified, e.g. has, is, etc.
# uriPrefix → the URI prefix to be used, default ontology baseURI

objectProperties = [
    { # Climate change mitigation (mitigation summary & adaptation summary)
        'type': 1,
        'name': ['Mitigation summary', 'C2'],
        'domain': ['Mitigation summary', 'B2'],
        'range': ['Mitigation summary', 'C2'],
        'property_prefix': 'has'
    }
    # {
    #     'type':
    # }
]


