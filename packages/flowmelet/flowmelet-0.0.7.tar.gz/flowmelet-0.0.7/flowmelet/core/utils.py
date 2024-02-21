import yaml
import re
import shutil
import os
import sys

reserved_keywords = ["operator", "dependencies", "original_dependencies", "execution_rule", "target_pattern"]
yml_to_python_supported_objects = ["None"]

def merge_dicts(dict1, dict2):
    result = dict1.copy()

    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value

    return result
    
def traverse_recursive(data, callback):
    if isinstance(data, dict):
        for key, value in data.items():
            callback(data, key, value)
            traverse_recursive(value, callback)
    elif isinstance(data, list):
        for item in data:
            callback(data, item)
            traverse_recursive(item, callback)

def extract_task_expression_content(sql_query):
    contents_single_qoutes = re.findall(r"\${\s*task\['([^']+?)'\].+\s*}", sql_query)
    contents_double_qoutes = re.findall(r"""\${\s*task\["([^']+?)"\].+\s*}""", sql_query)
    contents = [*[content.strip() for content in contents_single_qoutes], *[content.strip() for content in contents_double_qoutes]]
    return list(set(contents))
    
def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

def to_string(file_path):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        return file_content
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def execute_file_as_function(file_path, function_name):
    with open(file_path, 'r') as file:
        file_content = file.read()
    namespace = {}
    exec(file_content, namespace)
    if function_name in namespace:
        return namespace[function_name]
    else:
        raise AttributeError(f"Function '{function_name}' not found in the file.")


def extract_task_content(sql_query):
    contents = re.findall(r'\{\{(.*?)\}\}', sql_query)
    return [content.strip() for content in contents]

def replace_function_name(original_function_string, new_function_name):
    # Define a regex pattern to match function names
    pattern = r"def\s+(\w+)\s*\("

    # Use re.sub to replace the function name
    modified_function_string = re.sub(pattern, f"def {new_function_name}(", original_function_string, count=1)

    return modified_function_string

def extract_function_name(function_string):
    # Define a regex pattern to match function names
    pattern = r"def\s+(\w+)\s*\("

    # Use re.search to find the first match
    match = re.search(pattern, function_string)

    # Check if a match is found and return the function name
    if match:
        return match.group(1)
    else:
        return None

def copy_method(m):
    return types.MethodType(m.__func__, m.__self__)

def file_read(path):
    with open(path) as file:
        return file.read()

def file_write(content, path):
    folder_path = os.path.dirname(path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(path, 'w') as file:
        file.write(content)


def to_dict(path):
    with open(path) as file:
        return yaml.load(file, Loader=yaml.FullLoader)
    return {}
