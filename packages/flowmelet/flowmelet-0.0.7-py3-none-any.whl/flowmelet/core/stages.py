import os
from jinja2 import Environment, FileSystemLoader
from flowmelet.core import utils
import yaml
import re
import json

# TASKS_BAGS
def fill_tasks_bags(tree, dag_node, parent_node, current_node, child_nodes):
    is_a_task = current_node.type == 'task'
    is_a_dag = current_node.type == 'dag'
    if is_a_task or is_a_dag:
       tree.root.data['tasks_bags'] = tree.root.data['tasks_bags'] if 'tasks_bags' in tree.root.data else {}
       tree.root.data['tasks_bags'][current_node.node_id] = current_node.data


# TEMPLATE TASK INJECTION
def template_task_injection(tree, dag_node, parent_node, current_node, child_nodes):
    is_a_template = current_node.type == 'template'
    if is_a_template:
        target_pattern = current_node.data['target_pattern']
        found_node = tree.find_node_by_id(target_pattern)
        del current_node.data['target_pattern']
        if found_node is not None:
            found_node.data = utils.merge_dicts(found_node.data, current_node.data)
            tree.save_child_by_parent_id(parent_node.node_id, found_node.node_id, found_node.name, found_node.path, found_node.data)
        else:
            def inner_traverse(inner_tree, find_dag_node, find_parent_node, find_current_node, find_child_nodes):
                inner_is_a_task = find_current_node.type == 'task'
                if inner_is_a_task and re.search(target_pattern, yaml.dump(find_current_node.data)):
                    find_current_node.data = utils.merge_dicts(find_current_node.data, current_node.data)
            parent_node.traverse(tree, callback=inner_traverse)


# ENRICH TASK DEPENDENCIES FROM TASKS EXPRESSIONS
def enrich_task_dependencies_from_task_expressions(tree, dag_node, parent_node, current_node, child_nodes):
    is_a_task = current_node.type == 'task'
    if is_a_task:
        for attr_key, attr_value in current_node.data.copy().items():
            is_not_dependencies = 'dependencies' != attr_key
            if is_not_dependencies:
                string_content = yaml.dump(attr_value) if (isinstance(attr_value, list) or isinstance(attr_value, dict)) else str(attr_value)
                existing_dependencies = current_node.data['dependencies'] if 'dependencies' in current_node.data else []
                existing_dependencies = list(set([*existing_dependencies, *[dep.replace(f"{parent_node.node_id}{os.sep}","") if len(dep.replace(parent_node.node_id,"").split(os.sep)) == 2 else dep for dep in utils.extract_task_expression_content(string_content)]]))
                current_node.data['dependencies'] = existing_dependencies

# EVALUATE TASKS EXPRESSIONS
def evaluate_tasks_expressions(tree, dag_node, parent_node, current_node, child_nodes):
    is_a_task = current_node.type == 'task'
    if is_a_task:
        for attr_key, attr_value in current_node.data.copy().items():
            is_not_dependencies = 'dependencies' != attr_key
            if is_not_dependencies and (isinstance(attr_value, list) or isinstance(attr_value, dict)):
                def callback(data, key_or_item, value=None):
                    if value is not None and isinstance(value, str):
                        try:
                            rendered_value = tree.jinja_env.from_string(value).render(task=tree.root.data['tasks_bags'])
                            data[key_or_item] = yaml.load(rendered_value, Loader=yaml.FullLoader)
                        except Exception as e:
                            print(f"Unsupported task inheritance ${key_or_item}")
                utils.traverse_recursive(attr_value, callback)
                current_node.data[attr_key] = attr_value
            elif is_not_dependencies and isinstance(attr_value, str):
                try:
                    rendered_value = tree.jinja_env.from_string(attr_value).render(task=tree.root.data['tasks_bags'])
                    current_node.data[attr_key] = yaml.load(rendered_value, Loader=yaml.FullLoader)
                except Exception as e:
                    print(f"Unsupported task inheritance ${attr_key}")
            elif is_not_dependencies and isinstance(attr_value, str):
                string_content = attr_value
                rendered_value = tree.jinja_env.from_string(string_content).render(task=tree.root.data['tasks_bags'])
                current_node.data[attr_key] = rendered_value

# EVALUATE VALIDATIONS
def evaluate_validations(tree, dag_node, parent_node, current_node, child_nodes):
    is_a_validation = current_node.type == 'validation'
    if is_a_validation:
        func_name = utils.extract_function_name(utils.to_string(current_node.path))
        func = utils.execute_file_as_function(current_node.path, func_name)
        def find_and_validate_children(inner_tree, inner_dag_node, inner_parent_node, inner_current_node, inner_child_nodes):
            inner_current_node_is_a_task = inner_current_node.type == 'task'
            inner_current_node_is_a_dag = inner_current_node.type == 'dag'
            is_not_injected_task = "__" not in inner_current_node.node_id
            if (inner_current_node_is_a_task or inner_current_node_is_a_dag) and is_not_injected_task:
                func(inner_tree.root.data['tasks_bags'], inner_current_node.node_id, inner_current_node.type, {**inner_current_node.data, 'task_id': inner_current_node.node_id})
        parent_node.traverse(tree,callback=find_and_validate_children)

# INJECT EXTERNAL SENSOR TASK VIRTUAL NODES
def inject_external_sensor_tasks(tree, dag_node, parent_node, current_node, child_nodes):
    is_a_task = current_node.type == 'task'
    if is_a_task and 'dependencies' in current_node.data:
        for dependency in current_node.data['dependencies']:
            is_external_dag_task = os.sep in dependency
            find_node_id = dependency if is_external_dag_task else os.path.join(parent_node.node_id, dependency)
            dependency_node = tree.find_node_by_id(find_node_id)
            if dependency_node is None:
                raise ValueError(f"[TASK_NOT_FOUND]: {dependency}")
            if is_external_dag_task:
               sensor_task_name = f"___sensor_{dependency.replace(os.sep,'_')}"
               sensor_task_node_id = os.path.join(parent_node.node_id, sensor_task_name)
               sensor_task_path = os.path.join(parent_node.path, sensor_task_name)
               sensor_template_path = os.path.join(tree.template_path, "ExternalTaskSensorTemplate.yml")
               if dependency_node.type == "task":
                   external_dag_id = dependency_node.parent_node.node_id.replace(os.sep, "_")
                   external_task_id = dependency_node.name
               else:
                   external_dag_id = dependency_node.node_id.replace(os.sep, "_")
                   external_task_id = None
               sensor_config = {'task_id': sensor_task_name, 'external_dag_id': external_dag_id, 'external_task_id': external_task_id}
               sensor_template_rendered = Environment(loader=FileSystemLoader("templates/")).from_string(utils.file_read(sensor_template_path)).render(sensor_config)
               sensor_operator_config = yaml.safe_load(sensor_template_rendered)
               current_node.data["original_dependencies"] = current_node.data["original_dependencies"] if "original_dependencies" in current_node.data else current_node.data['dependencies']
               sensor_operator_config['dependencies'] = [dep for dep in current_node.data["original_dependencies"] if os.sep not in dep]
               current_node.data['dependencies'] = [dep for dep in current_node.data['dependencies'] if os.sep not in dep and ('__' in dep and dep != dependency)]
               current_node.data['dependencies'].append(sensor_task_name)
               tree.save_child_by_parent_id(parent_node.node_id, sensor_task_node_id, sensor_task_name, sensor_task_path, sensor_operator_config)


# INJECT DECORATOR TASKS VIRTUAL NODES
def inject_decorator_tasks(tree,dag_node, parent_node, current_node, child_nodes):
    is_a_task = current_node.type == 'task'
    is_a_decorator = current_node.type == 'decorator'
    if is_a_decorator:
        decorator_node = current_node
        target_pattern = decorator_node.data['target_pattern']
        found_node = tree.find_node_by_id(target_pattern)
        def inject_node(scope_tree, decorator_node, target_node, parent_target_node):
            execution_rule = decorator_node.data['execution_rule'] if 'execution_rule' in decorator_node.data else 'after'
            decorator_task_name = f"___decorator_{decorator_node.name.replace('.decorator','')}_{target_node.name}"
            rendered_decorator_task_config = yaml.load(tree.jinja_env.from_string(yaml.dump(decorator_node.data)).render(dag={ **parent_target_node.data, 'dag_id': parent_target_node.node_id }, task={**target_node.data, 'task_id':target_node.name}), Loader=yaml.FullLoader)
            decorator_task_node_id = os.path.join(parent_target_node.node_id, decorator_task_name)
            decorator_task_path = os.path.join(parent_target_node.path, decorator_task_name)
            if execution_rule == "after":
                rendered_decorator_task_config['dependencies'] = [target_node.name]
            else:
                target_node.data['dependencies'] = target_node.data['dependencies'] if 'dependencies' in target_node.data else []
                target_node.data['dependencies'] = [dep for dep in target_node.data['dependencies'] if dep != decorator_task_name]
                target_node.data['dependencies'].append(decorator_task_name)
            scope_tree.save_child_by_parent_id(parent_target_node.node_id, decorator_task_node_id, decorator_task_name, decorator_task_path, rendered_decorator_task_config)

        if found_node is not None:
            inject_node(tree, decorator_node, found_node, found_node.parent_node)
        else:
            def find_and_inject_decorator_task(inner_tree, find_dag_node, find_parent_node, find_current_node, find_child_nodes):
                current_node_is_a_task = find_current_node.type == 'task'
                is_not_injected_task = "___" not in find_current_node.name
                if(is_not_injected_task and current_node_is_a_task and re.search(decorator_node.data["target_pattern"], yaml.dump(find_current_node.data))):
                    inject_node(inner_tree, decorator_node, find_current_node, find_parent_node)
            parent_node.traverse(tree,callback=find_and_inject_decorator_task)

# CLEAN UP UNNECESSARY VIRTUAL NODES
def clean_up_unnecessary_nodes(tree, dag_node, parent_node, current_node, child_nodes):
    is_a_decorator = current_node.type == 'decorator'
    if is_a_decorator:
        parent_node.remove_child_by_id(current_node.node_id)
        tree.traverse_all_nodes(callback=clean_up_unnecessary_nodes)


# CONSTRUCT DAG CONFIG
def construct_dag_config(tree, dag_node, parent_node, current_node, child_nodes):
    is_a_task = current_node.type == 'task'
    if is_a_task:
        parent_node.data["tasks"] = parent_node.data["tasks"] if "tasks" in parent_node.data else {}
        parent_node.data["tasks"][current_node.name] = current_node.data


# CONSTRUCT PYTHON DAG
def construct_python_dag(tree, dag_node, parent_node, current_node, child_nodes):
    is_a_dag = current_node.type == 'dag'
    if is_a_dag:
        operators = {value["operator"]:value["operator"] for key, value in current_node.data["tasks"].items()}
        imports = [f'from {key.replace("."+key.split(".")[len(key.split("."))-1], "")} import {key.split(".")[len(key.split("."))-1]}' for key, value in operators.items()]
        dag_name = current_node.name
        dag_params = []
        for key, value in current_node.data.items():
            if key != "tasks":
                if isinstance(value, str) and value in utils.yml_to_python_supported_objects:
                    dag_params.append(f'{key}="""{value}"""')
                else:
                    dag_params.append(f'{key}={value}')
        tasks = []
        for key, value in current_node.data["tasks"].items():
            id = key
            operator = value["operator"].split(".")[len(value["operator"].split("."))-1]
            if operator != "PythonOperator":
                operator_params = []
                for operator_param_key, operator_param_value in value.items():
                    if operator_param_key not in utils.reserved_keywords:
                        if operator_param_value in utils.yml_to_python_supported_objects or isinstance(operator_param_value, int) or isinstance(operator_param_value, bool) or isinstance(operator_param_value, list) or isinstance(operator_param_value, dict):
                            operator_params.append(f'{operator_param_key}={operator_param_value}')
                        else:
                            operator_params.append(f'{operator_param_key}="""{operator_param_value}"""')
                tasks.append({'id': id, 'operator': operator, 'operator_params': operator_params})
            else:
                operator_params = []
                for operator_param_key, operator_param_value in value.items():
                    if operator_param_key != "operator" and operator_param_key != "python_callable" and operator_param_key != "dependencies" and operator_param_key != "original_dependencies":
                        if isinstance(operator_param_value, int) or isinstance(operator_param_value, bool) or isinstance(operator_param_value, list) or isinstance(operator_param_value, dict):
                            operator_params.append(f'{operator_param_key}={operator_param_value}')
                        else:
                            operator_params.append(f'{operator_param_key}="""{operator_param_value}"""')
                python_function_name = f'{id}_function'
                operator_params.append(f'python_callable={python_function_name}')
                tasks.append({'id': id, 'operator': operator, 'operator_params': operator_params, 'python_callable': utils.replace_function_name(value['python_callable'], python_function_name)})
        vertices = []
        for key, value in current_node.data["tasks"].items():
            if "dependencies" in value:
                for dependency in value["dependencies"]:
                   vertices.append({'A': dependency, 'B': key})
        rendered_python_dag = Environment(loader=FileSystemLoader("templates/")).from_string(utils.file_read(os.path.join(tree.template_path, "DAGTemplate.py"))).render(imports=imports, dag_name=dag_name, dag_params=dag_params, tasks=tasks, vertices=vertices)
        destination_path = os.path.join(tree.target_path, parent_node.node_id, f"{current_node.name}.out.py")
        if not os.path.exists(destination_path):
           utils.file_write(rendered_python_dag, destination_path.replace(f"root{os.sep}",""))


def write_lineage(tree, dag_node, parent_node, current_node, child_nodes):
    is_a_dag = current_node.type == 'dag'
    is_a_task = current_node.type == 'task'
    if is_a_dag:
        lineage = { 'nodes': [], 'edges': [] }
        nodes = {}
        edges = {}
        def inner_traverse(inner_tree, find_dag_node, find_parent_node, find_current_node, find_child_nodes):
            inner_is_a_dag = find_current_node.type == 'dag'
            inner_is_a_task = find_current_node.type == 'task'
            if inner_is_a_task or inner_is_a_dag:
                nodes[find_current_node.node_id] = {'data':find_current_node.data, 'type': find_current_node.data['operator'] if inner_is_a_task else find_current_node.type }
                if 'dependencies' in find_current_node.data:
                    for dep in find_current_node.data['dependencies']:
                        edges[os.path.join(find_parent_node.node_id,dep)] =  {find_current_node.node_id: find_current_node.node_id}
        current_node.traverse(tree, callback=inner_traverse)
        final_edge = []
        for edge_key, edge_value in edges.items():
            for edge_value_key, edge_value_value in edge_value.items():
                final_edge.append({'data': { 'source':edge_key, 'target': edge_value_key }})
        lineage = { 'nodes': [{'data': { 'id':key, 'description': yaml.dump(value), 'type': value['type'], 'json_data': json.dumps(value, indent=2) }} for key,value in nodes.items()], 'edges': final_edge }
        rendered_lineage = Environment(loader=FileSystemLoader("templates/")).from_string(utils.file_read(os.path.join(tree.template_path, "LineageTemplate.html"))).render(config=lineage)
        destination_path = os.path.join(tree.target_path, parent_node.node_id, f"{current_node.name}.out.html")
        utils.file_write(rendered_lineage, destination_path.replace(f"root{os.sep}",""))


def write_dag_factory_dag(tree, dag_node, parent_node, current_node, child_nodes):
    if current_node.type == "dag":
       dag_config = { current_node.node_id.replace(os.sep, '_'): current_node.data }
       rendered_dag_factory_config = Environment(loader=FileSystemLoader("templates/")).from_string(utils.file_read(os.path.join(tree.template_path, "DAGFactoryTemplate.py"))).render(dag_yml=yaml.dump(dag_config))
       destination_path = os.path.join(tree.target_path, parent_node.node_id, f"{current_node.name}.dagfactory.out.py")
       utils.file_write(rendered_dag_factory_config, destination_path.replace(f"root{os.sep}",""))

def write_nodes_configs_to_files(tree,dag_node, parent_node, current_node, child_nodes):
    if current_node.type == "dag" or current_node.type == "task":
       destination_path = os.path.join(tree.target_path, parent_node.node_id, f"{current_node.name}.out")
       utils.file_write(yaml.dump(current_node.data), destination_path.replace(f"root{os.sep}",""))


