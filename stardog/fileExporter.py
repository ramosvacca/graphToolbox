import stardog
from subprocess import *

fileName='/media/newbuntu/rdfal/ckgUpdated.ttl'

conn_details = {
  'endpoint': 'http://localhost:4322',
  'username': 'admin',
  'password': 'admin'
}

with stardog.Connection('ckgComplete', **conn_details) as conn:
    exportData = conn.export(graph_uri='urn:dev:ckg:data')
    file = open(fileName, 'w+')
    file.write(exportData.decode("utf-8"))

