base_uri_prefix = "otgs"
base_uri = "<http://mdata.com{}>"
# Initialize ontology in Turtle format
# Prefixes are required for the correct interpretation of the ontology
ttl_init = f"""
@prefix {base_uri_prefix}: <http://mdata.com/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix BFO: <http://purl.obolibrary.org/obo/BFO_> .


{base_uri_prefix}:isPartOf owl:equivalentProperty BFO:0000050 .
"""

base_path = '/media/newbuntu/rdfal/NEW AGE/OpenTargets/'

rdf_write_path = '/media/newbuntu/rdfal/NEW AGE/OpenTargets/RDF_data/'

csv_write_path = base_path+'csv_data/'



main_data =[
            # {'main_entity':'Evidence', 'data_path':'Data/Target - Disease evidence/evidence/', 'name_to_save':'sourceId=cancer_biomarkers'},
            {'main_entity':'Disease', 'data_path':'Data/Disease_Phenotype/', 'name_to_save':'diseases'},
            # {'main_entity':'Target', 'data_path':'Data/Target/', 'name_to_save':'targets'},
            # {'main_entity':'HumanPhenotype', 'data_path':'Data/Human Phenotype Ontology/', 'name_to_save':'hpo'},
            # {'main_entity':'ClinicalSignsAndSymptoms', 'data_path':'Data/ClinicalSignsAndSymptoms/', 'name_to_save':'diseaseToPhenotype'},
            # {'main_entity':'AssociationByOverallDirect', 'data_path':'Data/Target - Disease associations/', 'name_to_save':'associationByOverallDirect'},
            ]


type_prefixes = {'Drug'      :   ('CHEMBL'),
            'Disease'   :   ('EFO_', 'MONDO_', 'GO_', 'DOID_', 'Orphanet_', 'OTAR_', 'HP_', ),
            'Target'    :   ('ENS')
            }

predicate_exclude_types = ['name', 'id']