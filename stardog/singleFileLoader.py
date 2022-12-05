import stardog
from os.path import exists

fileNameDRUGS='/media/newbuntu/rdfal/drugs_construct/drugs_DRUGS.ttl'
fileNameINTERACTIONS='/media/newbuntu/rdfal/drugs_construct/drugs_INTERACTIONS.ttl'
fileNameCHEBI='/media/newbuntu/rdfal/CHEBI/owlapi.owl'
fileNameDRON='/media/newbuntu/rdfal/DRON/dron_original.rdf'
fileNameRXNORM_DRON='/media/newbuntu/rdfal/drugs_RXNORM_DRON_2.ttl'

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

# start loader 17:11
# end loader 19:
#replace { → (   &   } → )     &    \>  →
with stardog.Connection('drugs-nov11', **conn_details_2) as conn:

    if exists(fileNameRXNORM_DRON):
        conn.begin()
        print('connection started')
        conn.add(stardog.content.File(fileNameRXNORM_DRON, content_type='text/turtle'), graph_uri='urn:dev:drugs:data')
                                      #content_type='application/rdf+xml'), graph_uri='urn:dev:dron:data')
        print('conn.add')
        conn.commit()
        print('conn.commit ' + fileNameRXNORM_DRON)