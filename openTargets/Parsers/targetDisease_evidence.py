import re
import pandas as pd
import os
import json
import csv
from rdflib import Literal
from helper_functions import *
import field_explorer

# csv_config_path = '/media/newbuntu/rdfal/NEW AGE/OpenTargets/Config_files/target_disease.csv'
main_data =[{'name':'Evidence', 'data_path':'/media/newbuntu/rdfal/NEW AGE/OpenTargets/Data/Target - Disease evidence/evidence/sourceId=cancer_gene_census'}

]
data_path = '/media/newbuntu/rdfal/NEW AGE/OpenTargets/Data/Human Phenotype Ontology/hpo'
write_path = '/media/newbuntu/rdfal/NEW AGE/OpenTargets/RDF_data/'

main_dict = {}

# Define variables for URIs
base_uri_prefix = "otgs"
#class_uri = "otgs"

type_triple = "{} rdf:type {} .\n"
base_triple = "{} <http://mdata.com/{}> {} .\n"
base_uri = "<http://mdata.com{}>"
# class_uri = "<http://mdata.com/{}>"
empty_triple = "{} {} {} .\n"

# Initialize ontology in Turtle format
# Prefixes are required for the correct interpretation of the ontology
turtle = f"""
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

filepaths = {
             'molecule':'molecule/',
            'indications':'indication/',
             'mechanismofaction':'mechanismOfAction/',
             'drugwarnings':'fda/drugWarnings/',
             'significantreactions':'fda/significantAdverseDrugReactions/'
             }




def process_row(current_row, properties_array, is_auto_id, auto_id_counter, row_base_uri, current_entity_full_name, ttl_file, parent_entity=None):
    print(current_row)
    # remove prefix from current_entity_full_name
    base_entity_name = remove_baseURI_prefix(current_entity_full_name)
    # format the URI for this entity, from the base URI
    base_entity_uri = row_base_uri.format('/' + capital_first_char(base_entity_name) + '{}')

    # if automatic id is enabled, use auto_id_counter as row id; otherwise, use the 'id' field from the row
    row_id = str(auto_id_counter) if is_auto_id else str(current_row['id'])

    # format the row URI and type triple, then print the triple
    instance_uri = base_entity_uri.format('/' + row_id + '{}')
    row_type_triple = type_triple.format(instance_uri.format(''), base_uri.format('/' + capital_first_char(base_entity_name)))
    print(row_type_triple, file=ttl_file)

    if parent_entity is not None:
        print(empty_triple.format(base_uri.format('/' + parent_entity),
                                  base_uri.format('/' + base_entity_name), instance_uri.format('')), file=ttl_file)

    # iterate over key-value pairs in the row
    for key, value in current_row.items():

        if isinstance(value, dict):  # if the value is a nested dictionary
            # determine if the sub-entity needs an automatic id
            sub_is_auto_id = not any(prop_row[1] == key and prop_row[3] == 'id' for prop_row in properties_array)
            # recursively process the nested row
            process_row(value, properties_array, sub_is_auto_id, auto_id_counter, instance_uri, 'URI - ' + key,
                        ttl_file, parent_entity=capital_first_char(base_entity_name) + '/' + row_id)
        elif isinstance(value, list):  # if the value is a list of dictionaries
            print(value)
            # determine if the sub-entity needs an automatic id
            sub_is_auto_id = not any(prop_row[1] == key and prop_row[3] == 'id' for prop_row in properties_array)
            # initiate a counter for the sub-entities
            sub_auto_id_counter = 0
            parent_entity = str(parent_entity) if parent_entity is not None else ''
            current_entity_suffix = str(parent_entity) + capital_first_char(base_entity_name) + '/' + row_id

            # process each dictionary in the list
            for sub_row in value:
                if isinstance(sub_row, dict):
                    process_row(sub_row, properties_array, sub_is_auto_id, sub_auto_id_counter, instance_uri, 'URI - ' + key,
                                ttl_file, parent_entity= current_entity_suffix)

                else:  # if the value is a normal field
                    # format the predicate and object, then print the triple
                    item_predicate = base_uri.format('/' + key)
                    item_object = comillas(sub_row)
                    print(empty_triple.format(instance_uri.format(''), item_predicate, item_object), file=ttl_file)
                sub_auto_id_counter += 1
        else:  # if the value is a normal field
            # format the predicate and object, then print the triple
            item_predicate = base_uri.format('/' + key)
            item_object = comillas(value)
            print(empty_triple.format(instance_uri.format(''), item_predicate, item_object), file=ttl_file)

for folder_data in main_data:
    folder_count = 0
    print('Starting properties extraction process')
    properties_array = field_explorer.get_output(type_of_output='list', eval_path=folder_data['data_path'], level_name=folder_data['name'])
    print('Properties array -> OK')

    # Initial call
    base_entity_full_name = next(row[1] for row in properties_array if row[0] == 1)
    auto_id_n = 0
    base_auto_id = not any(
        prop_row[1] == base_entity_full_name and prop_row[3] == 'id' for prop_row in properties_array)

    # Look for all possible filepaths inside the current working directory and makes a list
    file_paths = [os.path.join(dirpath, file_name) for dirpath, _, files in os.walk(folder_data['data_path']) for file_name in
                  files if file_name.endswith(".json")]

    # Open the output file in write mode
    with open(f'{write_path}{folder_data["name"]}_{folder_count}.ttl', 'w') as output_file:
        # Iterate over file_paths
        for file_path in file_paths:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for row in lines:
                    row = json.loads(row)
                    # Pass the output file to the process_row function
                    process_row(row, properties_array, base_auto_id, auto_id_n, base_uri, base_entity_full_name, output_file)

    folder_count += 1