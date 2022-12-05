import stardog
from subprocess import *
import requests
from requests.auth import HTTPBasicAuth

baseUrl = 'http://localhost:7474/rdf/graph.db/describe/'

for i in range(1489,1545):
    beginInt = (i-1)*10000
    endInt = i*10000
    fileName = '/media/newbuntu/rdfal/ckg/ckg'+str(beginInt)+'to'+str(endInt)+'.rdf'
    file = open(fileName, 'w+')
    for nodeId in range(beginInt,endInt):
        requestUrl = baseUrl + str(nodeId)
        # Making a get request
        response = requests.get(requestUrl, auth=HTTPBasicAuth('neo4j', 'NeO4J'))
        file.write(response.text)
        if nodeId % 100 == 0:
            print('Finished node '+str(nodeId))
    print('finished from '+str((i-1)*10000)+'to'+str(i*10000))

"""
conn_details = {
  'endpoint': 'http://localhost:4322',
  'username': 'admin',
  'password': 'admin'
}

with stardog.Connection('nquadsSubset', **conn_details) as conn:
    exportData = conn.export(graph_uri='http://graph.mazetx.com/sightline-discovery')
    file = open(fileName, 'w+')
    file.write(exportData.decode("utf-8"))

"""