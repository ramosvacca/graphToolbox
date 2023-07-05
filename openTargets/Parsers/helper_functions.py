base_uri = "<http://mdata.com/{}>"


# class_uri = "<http://mdata.com/{}>"
def capital_first_char(word):
    return word[0].upper() + word[1:]

def comillas(inputText):
    return '"' + str(inputText) + '"'

def remove_baseURI_prefix(input_text):
    if input_text.startswith('baseURI'):
        return input_text.replace('baseURI:','').strip()
    elif input_text.startswith('URI -'):
        return input_text.replace('URI -','').strip()
    else:
        return input_text

def replace_baseURI_prefix(input_text):
    if input_text.startswith('baseURI'):
        return base_uri.format(input_text.replace('baseURI:','').strip())
    elif input_text.startswith('classURI'):
        return class_uri.format(input_text.replace('classURI:','').strip())
    elif input_text.startswith('URI -'):
        return base_uri.format(input_text.replace('URI -','').strip())
    else:
        return input_text

def list_to_string(input_text):
    if isinstance(input_text, list):
        return ','.join(input_text)
    elif isinstance(input_text, dict):
        # Use a list comprehension to convert the dictionary keys and values to strings,
        # Capitalize the first letter of each key, and join them together with ": " and ". "
        return '. '.join([f'{k.capitalize()}: {list_to_string(v)}' for k, v in input_text.items()])

    else:
        return input_text

def rdf_encode(input_text):
    if isinstance(input_text, str):
        input_text = input_text.replace("\\",'\\\\')
        return input_text.replace('"', r'\"')
    else:
        return input_text