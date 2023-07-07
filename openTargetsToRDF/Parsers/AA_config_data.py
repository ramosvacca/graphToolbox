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
            # {'main_entity':'Evidence', 'data_path':'Data/Target - Disease evidence/evidence/', 'name_to_save':None},
            # {'main_entity':'Disease', 'data_path':'Data/Disease_Phenotype/', 'name_to_save':'diseases'},
            # {'main_entity':'Target', 'data_path':'Data/Target/targets', 'name_to_save':'targets'},
            # {'main_entity':'GoAnnotation', 'data_path':'Data/Target/go', 'name_to_save':'target_go_annotation'},
            # {'main_entity':'BaselineExpression', 'data_path':'Data/Target/baselineExpression', 'name_to_save':'target_baseline_expression'},
            # {'main_entity':'MolecularInteraction', 'data_path':'Data/Target/interaction', 'name_to_save':'target_molecular_interaction'},
            # {'main_entity':'InteractionEvidence', 'data_path':'Data/Target/interactionEvidence', 'name_to_save':'target_molecular_interaction_evidence'},
            # {'main_entity':'MousePhenotype', 'data_path':'Data/Target/mousePhenotypes', 'name_to_save':'target_mouse_phenotypes'},
            # {'main_entity':'HumanPhenotype', 'data_path':'Data/Human Phenotype Ontology/', 'name_to_save':'hpo'},
            # {'main_entity':'ClinicalSignsAndSymptoms', 'data_path':'Data/ClinicalSignsAndSymptoms/', 'name_to_save':'diseaseToPhenotype'},
            # {'main_entity':'AssociationByOverallDirect', 'data_path':'Data/Target - Disease associations/', 'name_to_save':'associationByOverallDirect'},
            {'main_entity':'AssociationByOverallIndirect', 'data_path':'Data/Target - Disease associations/associationByOverallIndirect', 'name_to_save':'associationByOverallIndirect'},
            {'main_entity':'AssociationByDatasourceDirect', 'data_path':'Data/Target - Disease associations/associationByDatasourceDirect', 'name_to_save':'associationByDatasourceDirect'},
            {'main_entity':'AssociationByDatatypeDirect', 'data_path':'Data/Target - Disease associations/associationByDatatypeDirect', 'name_to_save':'associationByDatatypeDirect'},
            {'main_entity':'AssociationByDatatypeIndirect', 'data_path':'Data/Target - Disease associations/associationByDatatypeIndirect', 'name_to_save':'associationByDatatypeIndirect'},
            {'main_entity':'AssociationByDatasourceIndirect', 'data_path':'Data/Target - Disease associations/associationByDatasourceIndirect', 'name_to_save':'associationByDatasourceIndirect'}
            ]

# Prefixes for each type of main entity in OpenTargets, Target, Drug and Disease or Phenotype.
type_prefixes = {'Drug'      :   ('CHEMBL'),
            'Disease'   :   ('EFO_', 'MONDO_', 'GO_', 'DOID_', 'Orphanet_', 'OTAR_', 'HP_', ),
            'Target'    :   ('ENS')
            }

# Predicates to exclude prefix conversion to entities when it's used
predicate_exclude_types = ['name', 'id']