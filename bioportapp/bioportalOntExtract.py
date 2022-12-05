import requests
import stardog
import os
import configparser
import ast

cwd = os.path.dirname(os.path.realpath(__file__))

config= configparser.ConfigParser()
config.read(cwd+'/config.ini')

sdLocalPort = config['SD']['port']
ontologies = ast.literal_eval(config['ONT']['list'])
apikey = {'apikey':config['BP']['apikey']}
database = config['SD']['database']
isNewDatabase = config['SD']['isNewDatabase']
sdUser = config['SD']['user']
sdPass = config['SD']['password']
graphUriBase = config['ONT']['graphUriBase']
conn_details = {
  'endpoint': 'http://localhost:'+sdLocalPort,
  'username': sdUser,
  'password': sdPass
}
print(apikey)

def ontDownloadImport(ontologies=ontologies, conn_details=conn_details, apikey=apikey, database=database,
                      isNewDatabase=isNewDatabase, graphUriBase=graphUriBase):

    with stardog.Admin(**conn_details) as admin:

        if isNewDatabase=='True':
            admin.new_database(database)

        for ontology in ontologies:
            print(ontology)
            print('check existance of '+ ontology + '.[ owl | ttl ]')
            fileName = cwd+'/ontologies/'+ontology
            # Check if the file exists in RDF or TTL, if it doesn't download is triggered

            if not ((os.path.exists(fileName+'.owl')) or (os.path.exists(fileName+'.ttl'))):
                print(fileName+' Ontology file does not exist, it will be downloaded.')
                # form the ontology URL to request the download
                ontologyURL = "https://data.bioontology.org/ontologies/"+ontology+"/download"
                data = requests.get(ontologyURL, params = apikey)
                # gets the first line of the ontology file
                firstLine = data.text.partition('\n')[0]

                if firstLine=='<?xml version="1.0"?>':
                    fileName += '.owl'
                else:
                    fileName += '.ttl'

                file = open(fileName, 'w+')
                file.write(data.text)

            elif (os.path.exists(fileName + '.owl')):
                fileName += '.owl'

            elif (os.path.exists(fileName + '.ttl')):
                fileName += '.ttl'

            with stardog.Connection(database, **conn_details) as conn:
                try:
                    conn.begin()
                    conn.add(stardog.content.File(fileName), graph_uri=graphUriBase+ontology)
                    conn.commit()
                    print('Ontology loaded from saved file: ' + fileName)
                except:
                    print('File was not loaded as RDF or TTL. Processing next Ontology')
                    continue
                    
                query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX obi: <http://purl.obolibrary.org/obo/OBI_>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
prefix scmt: <http://rdfal.com/#>
prefix dc: <http://purl.org/dc/elements/1.1/> 


SELECT DISTINCT ?strippedOntologyName ?strippedInfoType ?strippedData FROM <%s%s>
WHERE {

  ?ontology rdf:type owl:Ontology;
            ?p ?data;
            dc:title ?ontologyName .
  ?p rdfs:label ?infoType .
  
  BIND (STR(?ontologyName)  AS ?strippedOntologyName)
  BIND (STR(?infoType)  AS ?strippedInfoType)
  BIND (STR(?data)  AS ?strippedData)
}""" % (graphUriBase, ontology)
                results = conn.select(query)
                readmeFilePath = cwd + '/ontologies/' + ontology + 'Readme.txt'
                readmeFile = open(readmeFilePath, 'a+')
                readmeFile.write('/////// Information file for the ontology %s ///////\n\n' % ontology)

                for result in results['results']['bindings']:

                    readmeFile.write(result['strippedInfoType']['value']+': '+result['strippedData']['value']+'\n')
                print('readme file made for the ontology '+ontology)



    print('process success on database '+database)


ontDownloadImport()

