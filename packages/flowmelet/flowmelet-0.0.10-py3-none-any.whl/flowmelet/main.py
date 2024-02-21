import sys
import os
import yaml
import re
import json
import argparse
from flowmelet.core import utils
from flowmelet.core.system_tree import FileSystemTree
from flowmelet.core import stages
import argparse

def main():

    parser = argparse.ArgumentParser(description="Hello I'm Flowmelet the DAG generator.")
    parser.add_argument('--dags_path', help='Dags path')
    parser.add_argument('--mode', default='all', help='Modes: all - to generate all (Native DAGs, Lineages, Dagfactory Config DAGs, Debug Node Configs), native - to generate native dags, lineage - to generate lineage, dagfactory - to generate dagfactory dag, debug - to generate node configs, cleanup - to cleanup generated files')

    args = parser.parse_args()
    dags_path = args.dags_path
    mode = args.mode

    if(not os.path.exists(dags_path) and not os.path.isdir(dags_path)):
        raise ValueError(f"project_path={project_path} directory doesn't exists!")

    abs_path = sys.path[0]
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),  "templates")
    target_folder = os.path.join(project_path, "target")

    virtual_tree = FileSystemTree(template_path, dags_path, target_folder)
    virtual_tree.scan_directory(dags_path, virtual_tree.root)
    virtual_tree.print()

    utils.delete_folder(target_folder)
    
    if mode == "cleanup":
        return None

    all_stages = [
         stages.enrich_task_dependencies_from_task_expressions,
         stages.inject_external_sensor_tasks,
         stages.inject_decorator_tasks,
         stages.template_task_injection,
         stages.clean_up_unnecessary_nodes,
         stages.construct_dag_config,
         stages.fill_tasks_bags,
         stages.evaluate_tasks_expressions,
         stages.evaluate_validations
    ]

    if mode.lower() == "debug":
        all_stages = [*all_stages, stages.write_nodes_configs_to_files]
    elif mode.lower() == "native":
        all_stages = [*all_stages, stages.construct_python_dag]
    elif mode.lower() == "dagfactory":
        all_stages = [*all_stages, stages.write_dag_factory_dag]
    elif mode.lower() == "lineage":
        all_stages = [*all_stages, stages.write_lineage]
    else:
        all_stages = [*all_stages,
                 stages.construct_python_dag,
                 stages.write_lineage,
                 stages.write_dag_factory_dag,
                 stages.write_nodes_configs_to_files]

    for stage in all_stages:
      virtual_tree.traverse_all_nodes(callback=stage)
      #virtual_tree.print()



if __name__ == "__main__":
    main()
