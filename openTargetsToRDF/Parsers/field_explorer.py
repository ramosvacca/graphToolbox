
# Import Module
import os, json
import AA_config_data

#
# false = False
# Folder Path
save_path = '/media/newbuntu/rdfal/NEW AGE/OpenTargets/Data/Drug/molecule'

def capital_first_char(word):
    return word[0].upper() + word[1:]

# Read text File

prefixes = AA_config_data.type_prefixes

def read_text_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        file_set = dict()
        for line in lines:
            json_line = json.loads(line)
            # if json_line['chemblIds'] == ['CHEMBL786', 'CHEMBL83']:
            #     print(json_line)
            # print(json_line)
            for key, value in json_line.items():
                if key not in file_set:

                    file_set[key] = value

                elif key in file_set and type(value) == list and len(file_set[key]) < len(value) :

                    file_set[key] = value

        return file_set

def dict_to_csv(input=None, level=1, level_name=None, has_next_level=False):
    parent_level_name = 'URI - ' + level_name
    csv_output = []

    for key, value in input.items():
        #print(value)
        if type(value) is dict and 'rows' in value:
            value = value['rows']

        if type(value) is dict:
            has_next_level = True
            csv_output.append([level, parent_level_name, "", key, "", 'URI - ' + capital_first_char(key), value, has_next_level])
            # csv_output.append([level+1, 'URI - '+capital_first_char(key), 'URI', 'AUTO GENERATED','','','',''])
            csv_output += dict_to_csv(input=value, level=level + 1, level_name=capital_first_char(key), has_next_level=False )
        elif type(value) is list:
            if len(value) > 0 and isinstance(value[0], dict):
                has_next_level=True
                csv_output.append([level, parent_level_name, '', key, '', 'URI - ' + capital_first_char(key), value, has_next_level])
                # csv_output.append([level+1, 'URI - '+capital_first_char(key), 'URI', 'AUTO GENERATED', '', '', '', ''])
                csv_output += dict_to_csv(input=value[0], level=level + 1, level_name=capital_first_char(key), has_next_level=False )
            else:

                range = 'list'
                # Iterate over each entity type in the prefixes dictionary
                for entity_type in prefixes:
                    # Check if the string representation of t_object starts with the current prefix
                    if str(value[0]).startswith(prefixes[entity_type]):
                        # Format t_object by appending entity type and original t_object to base URI
                        # value = AA_config_data.base_uri.format(f'/{entity_type}/{value}')
                        range = 'URI - ' + entity_type
                        # Exit loop as a matching prefix has been found
                        break

                csv_output.append([level, parent_level_name, "", key, "", range, value, False])

                # csv_output.append([level, parent_level_name, '', key, '', 'list', value, False])
        elif type(value) is int:
            csv_output.append([level, parent_level_name, "", key, "", 'integer', value, False])
        elif type(value) is float:
            csv_output.append([level, parent_level_name, "", key, "", 'decimal', value, False])
        else:
            range = 'string'
            # Iterate over each entity type in the prefixes dictionary
            for entity_type in prefixes:
                # Check if the string representation of t_object starts with the current prefix
                if not key == 'id' and str(value).startswith(prefixes[entity_type]):
                    # Format t_object by appending entity type and original t_object to base URI
                    # value = AA_config_data.base_uri.format(f'/{entity_type}/{value}')
                    range = 'URI - ' + entity_type
                    # Exit loop as a matching prefix has been found
                    break

            csv_output.append([level, parent_level_name, "", key, "", range, value, False])
    return csv_output

def get_output(type_of_output='csv', eval_path=None, level_name=None, csv_save_folder=None, save_name=None):
    final_dict = dict()

    # Change the directory
    os.chdir(eval_path)

    for dirpath, dirs, files in os.walk(eval_path):
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(dirpath, file_name)
                # Call the function to read json file
                final_dict.update(read_text_file(file_path))
    output = dict_to_csv(input=final_dict, level_name=level_name)
    # Print the result

    to_print = 'level|parent|property_type|name_in_dataset|predicate|range|example|has_next_level\n'
    for row in output:
        to_print += ('|'.join(str(x) for x in row)) + '\n'

    if csv_save_folder is not None:
        with open(f'{csv_save_folder}{save_name}.csv', 'w') as output_file:
            output_file.write(to_print)

    if type_of_output == 'csv':
        return to_print

    else:
        return output
# Use the function to convert dictionary to the required CSV-like list of lists



# get_output()
# print(get_output(level_name='Drug'))


