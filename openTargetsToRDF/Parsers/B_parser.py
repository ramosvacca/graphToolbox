import os
import json
from AA_helper_functions import *
import field_explorer
import AA_config_data

# csv_config_path = '/media/newbuntu/rdfal/NEW AGE/OpenTargets/Config_files/target_disease.csv'
rdf_write_path = AA_config_data.rdf_write_path

main_dict = {}
main_data = AA_config_data.main_data
base_path = AA_config_data.base_path

csv_write_folder_path = AA_config_data.csv_write_path

type_triple = "{} rdf:type {} .\n"
base_triple = "{} <http://mdata.com/{}> {} .\n"
base_uri = "<http://mdata.com{}>"
# class_uri = "<http://mdata.com/{}>"
empty_triple = "{} {} {} .\n"

prefixes = AA_config_data.type_prefixes
exclude_convert_to_entity = AA_config_data.predicate_exclude_types


def triple_to_ttl(t_subject, t_predicate, t_object, print_file):
    """
    The purpose of this function is to format the object of a RDF triple, `t_object`, according to a set of predefined prefixes.
    The function tries to match the beginning of `t_object` with one of the predefined prefixes. If a match is found, it appends the
    entity type and the original `t_object` to a base URI. If no match is found, it simply prints a message. The final step is to print
    the RDF triple into a predefined format and write it to `print_file`.

    Args:
    t_subject (str): The subject of the RDF triple.
    t_predicate (str): The predicate of the RDF triple.
    t_object (str): The object of the RDF triple to be formatted.
    print_file (file object): The file object where the output will be written.
    """

    # Initialize a flag to track if a matching prefix has been found
    matched = False

    # Iterate over each entity type in the prefixes dictionary
    for entity_type in prefixes:
        # Check if the string representation of t_object starts with the current prefix
        if t_predicate not in exclude_convert_to_entity and str(t_object).startswith(prefixes[entity_type]):
            # Format t_object by appending entity type and original t_object to base URI
            t_object = base_uri.format(f'/{entity_type}/{t_object}')
            # Set flag to True indicating a match has been found
            matched = True
            # Exit loop as a matching prefix has been found
            break

    # If no matching prefix found, print a message
    if not matched:
        t_object = comillas(t_object)

    # Format and print the RDF triple, writing it to print_file
    print(empty_triple.format(t_subject, base_uri.format('/' + t_predicate), t_object), file=print_file)


def process_row(current_row, properties_array, is_auto_id, auto_id_counter, row_base_uri, current_entity_full_name, ttl_file, parent_entity=None):

    # remove prefix from current_entity_full_name
    base_entity_name = remove_baseURI_prefix(current_entity_full_name)
    # format the URI for this entity, from the base URI
    base_entity_uri = row_base_uri.format('/' + capital_first_char(base_entity_name) + '{}')

    # if automatic id is enabled, use auto_id_counter as row id; otherwise, use the 'id' field from the row
    print(current_row)
    row_id = str(auto_id_counter) if is_auto_id else str(current_row['id'])

    # format the row URI and type triple, then print the triple
    instance_uri = base_entity_uri.format('/' + row_id + '{}')
    row_type_triple = type_triple.format(instance_uri.format(''), base_uri.format('/' + capital_first_char(base_entity_name)))
    print(row_type_triple, file=ttl_file)

    if parent_entity is not None:
        # Check if the value is a dictionary and if 'rows' is in that dictionary
        if isinstance(current_row, dict) and 'rows' in current_row:
            for value in current_row['rows']:
                triple_to_ttl(base_uri.format('/' + parent_entity),
                                  base_entity_name, value, print_file=ttl_file)
            return
        else:
            print(empty_triple.format(base_uri.format('/' + parent_entity),
                                  base_uri.format('/' + base_entity_name), instance_uri.format('')), file=ttl_file)


    # iterate over key-value pairs in the row
    for key, value in current_row.items():

        if isinstance(value, dict):  # if the value is a nested dictionary

            # determine if the sub-entity needs an automatic id
            sub_is_auto_id = not any(prop_row[1] == key and prop_row[3] == 'id' for prop_row in properties_array)
            # recursively process the nested row
            # if parent_entity is not None:
            #     next_paren_entity = capital_first_char(base_entity_name) + '/' + row_id

            current_entity_suffix = str(parent_entity) + '/' + capital_first_char(base_entity_name) + '/' + row_id
            #
            process_row(value, properties_array, sub_is_auto_id, 0, instance_uri, 'URI - ' + key,
                        ttl_file, parent_entity=current_entity_suffix)

        elif isinstance(value, list):  # if the value is a list of dictionaries
            print(value)
            # determine if the sub-entity needs an automatic id
            sub_is_auto_id = not any(prop_row[1] == key and prop_row[3] == 'id' for prop_row in properties_array)
            # initiate a counter for the sub-entities
            sub_auto_id_counter = 0
            parent_entity = str(parent_entity) if parent_entity is not None else ''
            current_entity_suffix = str(parent_entity) + '/' + capital_first_char(base_entity_name) + '/' + row_id

            # process each dictionary in the list
            for sub_row in value:
                if isinstance(sub_row, dict):
                    process_row(sub_row, properties_array, sub_is_auto_id, sub_auto_id_counter, instance_uri, 'URI - ' + key,
                                ttl_file, parent_entity = current_entity_suffix)

                else:  # if the value is a list of strings, normal field
                    # format the predicate and object, then print the triple
                    # item_predicate = base_uri.format('/' + key)
                    item_object = sub_row
                    triple_to_ttl(instance_uri.format(''), key, item_object, ttl_file)
                    # print(empty_triple.format(instance_uri.format(''), item_predicate, item_object), file=ttl_file)
                sub_auto_id_counter += 1
        else:  # if the value is a normal field
            # format the predicate and object, then print the triple
            # item_predicate = base_uri.format('/' + key)
            item_object = value
            triple_to_ttl(instance_uri.format(''), key, item_object, ttl_file)
            # print(empty_triple.format(instance_uri.format(''), item_predicate, item_object), file=ttl_file)

def evaluate_folder(eval_path=None, level_name=None, save_name=None, auto_id_n=0):

    properties_array = field_explorer.get_output(type_of_output='list', eval_path=eval_path, level_name=level_name, csv_save_folder=csv_write_folder_path, save_name=save_name)
    print('Properties array -> OK')

    # Initial call
    base_entity_full_name = next(row[1] for row in properties_array if row[0] == 1)

    base_auto_id = not any(
        prop_row[1] == base_entity_full_name and prop_row[3] == 'id' for prop_row in properties_array)

    # Look for all possible filepaths inside the current working directory and makes a list

    file_paths = [os.path.join(dirpath, file_name) for dirpath, _, files in os.walk(eval_path) for file_name in
                  files if file_name.endswith(".json")]

    # Open the output file in write mode to save the rdf file with the data

    with open(f'{rdf_write_path}{folder_data["main_entity"]}_{save_name}.ttl', 'w') as output_file:
        # Iterate over file_paths
        for file_path in file_paths:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for row in lines:
                    row = json.loads(row)
                    # Pass the output file to the process_row function
                    process_row(row, properties_array, base_auto_id, auto_id_n, base_uri, base_entity_full_name, output_file)

                    auto_id_n += 1

    return auto_id_n

def get_subfolder_paths(directory):
    subfolder_paths = {}  # Stores the names and paths of subdirectories
    for name in os.listdir(directory):
        full_path = os.path.join(directory, name)
        if os.path.isdir(full_path):
            subfolder_paths[name] = full_path

    # Check if subfolder_paths dictionary is empty
    if not subfolder_paths:
        return False
    else:
        return subfolder_paths

for folder_data in main_data:

    auto_id_n = 0

    folder_path_to_evaluate = base_path+folder_data['data_path']

    subfolder_paths = get_subfolder_paths(folder_path_to_evaluate)

    if subfolder_paths:
        for name, path in subfolder_paths.items():
            print(name, path)
            # continue
            auto_id_n = evaluate_folder(eval_path=path, level_name=folder_data['main_entity'], save_name=name, auto_id_n=auto_id_n)

    else:
        folder_path_to_evaluate = folder_path_to_evaluate + folder_data['name_to_save']
        evaluate_folder(eval_path=folder_path_to_evaluate, level_name=folder_data['main_entity'], save_name=folder_data['name_to_save'])

