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
conn_details = {
  'endpoint': 'http://localhost:'+sdLocalPort,
  'username': sdUser,
  'password': sdPass
}
print(apikey)

def ontDownloadImport(ontologies=ontologies, conn_details=conn_details, apikey=apikey, database=database, isNewDatabase=isNewDatabase, sdPass=sdPass, sdUser=sdUser, sdLocalPort=sdLocalPort):

    with stardog.Admin(**conn_details) as admin:

        if isNewDatabase=='True':
        	db = admin.new_database(database)

        for ontology in ontologies:
            print('dowloading and saving '+ ontology)

            filename = cwd+'/ontologies/'+ontology+'.owl'
            ontologyURL = "https://data.bioontology.org/ontologies/"+ontology+"/download"

            data = requests.get(ontologyURL, params = apikey)

            file = open(filename, 'w+')
            file.write(data.text)

            with stardog.Connection(database, **conn_details) as conn:
                conn.begin()
                conn.add(stardog.content.File(filename))
                conn.commit()

            print('Ontology loaded from saved file: '+filename)

    print('process success on database '+database)


ontDownloadImport()