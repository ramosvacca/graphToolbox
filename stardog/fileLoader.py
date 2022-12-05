import stardog
from os.path import exists

filePath = '/media/newbuntu/rdfal/DrugBankData.ttl'

conn_details = {
  'endpoint': 'http://localhost:4322',
  'username': 'admin',
  'password': 'admin'
}

with stardog.Connection('ckgComplete', **conn_details) as conn:

    for i in range(51, 52):
        beginInt = (i - 1) * 10000
        endInt = i * 10000
        fileName = '/media/newbuntu/rdfal/ckg/unzipped[withdrugbank]/ckg' + str(beginInt) + 'to' + str(endInt) + '.rdf'
        print('TRY FILENAME IS ' + fileName)
        if exists(fileName):
            conn.begin()
            print('connection started')
            conn.add(stardog.content.File(fileName,content_type='text/turtle'),graph_uri='urn:dev:ckg:data')
            print('conn.add')
            conn.commit()
            print('conn.commit '+fileName)
