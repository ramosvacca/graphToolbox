import stardog
from os.path import exists

fileNameDRUGS='/media/newbuntu/rdfal/healthcareDemo/drugs_OPENTARGETS_.ttl'
fileNameDISEASES='/media/newbuntu/rdfal/healthcareDemo/diseases_OPENTARGETS.ttl'

conn_details = {
  'endpoint': 'http://localhost:4322',
  'username': 'admin',
  'password': 'admin'
}
conn_details_2 = {
'endpoint': 'https://solutions-demo.stardog.cloud:5820',
  'username': 'alexander.castro@stardog.com',
  'password': 'alex'
}

# with stardog.Connection('drugs-nov11', **conn_details_2) as conn:
#
#     if exists(fileNameDRUGS):
#         conn.begin()
#         print('connection started')
#         conn.add(stardog.content.File(fileNameDRUGS,content_type='text/turtle'),graph_uri='urn:dev:drugs:data')
#         print('conn.add')
#         conn.commit()
#         print('conn.commit '+fileNameDRUGS)
#
# with stardog.Connection('drugs-nov11', **conn_details_2) as conn:
#
#     if exists(fileNameINTERACTIONS):
#         conn.begin()
#         print('connection started')
#         conn.add(stardog.content.File(fileNameINTERACTIONS,content_type='text/turtle'),graph_uri='urn:dev:drugs:data')
#         print('conn.add')
#         conn.commit()
#         print('conn.commit '+fileNameINTERACTIONS)


with stardog.Connection('opentarget-drugs', **conn_details_2) as conn:

    if exists(fileNameDRUGS):
        conn.begin()
        print('connection started')
        conn.add(stardog.content.File(fileNameDRUGS, content_type='text/turtle'), graph_uri='urn:demo:healthcare:data')
                                      #content_type='application/rdf+xml'), graph_uri='urn:dev:dron:data')
        print('conn.add')
        conn.commit()
        print('conn.commit ' + fileNameDRUGS)

with stardog.Connection('opentarget-drugs', **conn_details_2) as conn:

    if exists(fileNameDISEASES):
        conn.begin()
        print('connection started')
        conn.add(stardog.content.File(fileNameDISEASES, content_type='text/turtle'), graph_uri='urn:demo:healthcare:data')
                                      #content_type='application/rdf+xml'), graph_uri='urn:dev:dron:data')
        print('conn.add')
        conn.commit()
        print('conn.commit ' + fileNameDISEASES)