# XLSX to TTL (RDF serialized)

Properties processing

Object Property → should be a list of dictionaries:
Each dictionary describes one property and should provide the following arguments:
type → 1 - Object Property, 2 - Datatype Property, 3 - Annotation Property
name → the name of the property as a reference list [sheet name, cell reference]
domain → it should be a reference to a cell or list of references to a cell [sheet name, cell reference]
range → it should be a reference to a cell or list of references to a cell [sheet name, cell reference] 
propertyPrefix → if the URI is to have a prefix, it should be specified, e.g. has, is, etc.
uriPrefix → the URI prefix to be used, default ontology baseURI

