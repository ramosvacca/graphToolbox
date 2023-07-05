
# Import Module
import os, json
false = False
# Folder Path
path = '/media/newbuntu/rdfal/NEW AGE/OpenTargets/Data/Target - Disease evidence/evidence/'

def capital_first_char(word):
    return word[0].upper() + word[1:]

# Read text File


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
        if type(value) is dict:
            has_next_level = True
            csv_output.append([level, parent_level_name, "", key, "", 'dict', value, has_next_level])
            # csv_output.append([level+1, 'URI - '+capital_first_char(key), 'URI', 'AUTO GENERATED','','','',''])
            csv_output += dict_to_csv(input=value, level=level + 1, level_name='URI - '+capital_first_char(key), has_next_level=False )
        elif type(value) is list:
            if len(value) > 0 and isinstance(value[0], dict):
                has_next_level=True
                csv_output.append([level, parent_level_name, '', key, '', 'list', value, has_next_level])
                # csv_output.append([level+1, 'URI - '+capital_first_char(key), 'URI', 'AUTO GENERATED', '', '', '', ''])
                csv_output += dict_to_csv(input=value[0], level=level + 1, level_name='URI - '+capital_first_char(key), has_next_level=False )
            else:
                csv_output.append([level, parent_level_name, '', key, '', 'list', value, False])
        elif type(value) is int:
            csv_output.append([level, parent_level_name, "", key, "", 'integer', value, False])
        elif type(value) is float:
            csv_output.append([level, parent_level_name, "", key, "", 'decimal', value, False])
        else:
            csv_output.append([level, parent_level_name, "", key, "", 'string', value, False])
    return csv_output

def get_output(type_of_output='csv', eval_path=path, level_name=None):
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
    if type_of_output == 'csv':
        to_print = 'level|parent|property_type|name_in_dataset|predicate|range|example|has_next_level\n'
        for row in output:
            to_print += ('|'.join(str(x) for x in row)) + '\n'
    else:
        return output
# Use the function to convert dictionary to the required CSV-like list of lists



#get_output()
#print(get_output('list'))


