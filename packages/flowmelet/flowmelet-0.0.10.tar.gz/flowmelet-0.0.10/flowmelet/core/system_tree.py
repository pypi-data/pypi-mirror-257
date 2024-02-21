import os
import re
from jinja2 import Environment, FileSystemLoader
from flowmelet.core import utils

def find_node_by_name(name, nodes):
    for node in nodes:
        if name == node.name:
           return node
    return None

class FileSystemNode:
    def __init__(self, name, node_id, path, type=None, data=None, parent_node=None):
        self.name = name
        self.node_id = node_id
        self.children = []
        self.path = path
        self.data = {}
        self.type = type
        self.parent_node = parent_node

        if data is not None:
            self.data = data

    def update_data(self, data={}):
        self.data = data

    def find_node_by_id(self, id):
        if self.node_id == id:
            return node
        else:
            for child in self.children:
                if child.node_id == id:
                    return child
                found_child = child.find_node_by_id(id)
                if found_child:
                    return found_child
        return None

    def find_node_by_ids(self, parent_id, child_id):
        if self.node_id == parent_id:
            for child in self.children:
                if child.node_id == child_id:
                    return child
                found_child = child.find_node_by_ids(parent_id, child_id)
                if found_child:
                    return found_child
        else:
            for child in self.children:
                found_child = child.find_node_by_ids(parent_id, child_id)
                if found_child:
                    return found_child
        return None

    def find_node_by_name(self, child_name, parent_id=None):
            if parent_id is None and self.name == child_name:
                return self
            elif parent_id is None:
                for child in self.children:
                    found_child = child.find_node_by_name(child_name)
                    if found_child:
                        return found_child
            elif self.node_id == parent_id:
                for child in self.children:
                    if child.name == child_name:
                        return child
                    found_child = child.find_node_by_name(child_name, parent_id)
                    if found_child:
                        return found_child
            else:
                for child in self.children:
                    found_child = child.find_node_by_name(child_name, parent_id)
                    if found_child:
                        return found_child
            return None

    def find_node_by_name_name(self, parent_name, child_name):
        if self.name == parent_name:
            for child in self.children:
                if child.name == child_name:
                    return child
                found_child = child.find_node_by_name_name(parent_name, child_name)
                if found_child:
                    return found_child
        else:
            for child in self.children:
                found_child = child.find_node_by_name_name(parent_name, child_name)
                if found_child:
                    return found_child
        return None

    def add_child(self, child_name, path, data=None, type=None):
        child_name = child_name.replace(".yml","")
        new_child = FileSystemNode(child_name, os.path.join(self.node_id, child_name),  path, type, data, self)
        self.children.append(new_child)
        return new_child

    def save_child(self, child_id, child_name, path, data=None, type=None):
        child_name = child_name.replace(".yml","")
        new_child = FileSystemNode(child_name, child_id,  path, type, data, self)
        self.children = [child for child in self.children if child.node_id != child_id]
        self.children.append(new_child)
        return new_child

    def inject_child_after_by_parent_id(self, child_id, child_name, path, data=None, type=None):
        child_already_exists = [child for child in self.children if child_id == child.node_id]
        if len(child_already_exists) > 0:
            return child_already_exists[0]

        child_name = child_name.replace(".yml","")
        new_child = FileSystemNode(child_name, child_id,  path, type, data, self)
        existing_injections = [child for child in self.children if "___" in child.name]
        if len(existing_injections) > 0:
            new_child.children = existing_injections[0].children
        else:
            new_child.children = self.children
        self.children = existing_injections
        self.children.append(new_child)
        return new_child

    def inject_child_before_by_parent_id(self, child_id, child_name, path, data=None, type=None):
        child_already_exists = [child for child in self.children if child_id == child.node_id]
        if len(child_already_exists) > 0:
            return child_already_exists[0]

        child_name = child_name.replace(".yml","")
        new_child = FileSystemNode(child_name, child_id,  path, type, data, self)
        existing_injections = [child for child in self.children if "___" in child.name]
        if len(existing_injections) > 0:
            new_child.children = existing_injections[0].children
        else:
            new_child.children = self.children
        self.children = existing_injections
        self.children.append(new_child)
        return new_child

    def add_child_by_id(self, child_name, node_id):
        for child in self.children:
            if child.node_id == node_id:
                new_child = FileSystemNode(child_name, str(uuid.uuid1()))
                child.children.append(new_child)
                return new_child
        return None

    def remove_child_by_id(self, node_id):
        for child in self.children:
            if child.node_id == node_id:
                self.children.remove(child)
                return child
        return None

    def remove_child_by_child_id(self, child_id):
        for child in self.children:
            if child.node_id == child_id:
                self.children.remove(child)
                return child
        return None

    def print(self, dag=None, parent=None, depth=0, callback=None, debug=False):
            if callback:
                callback(dag, parent, self, self.children)
            print("  " * depth + f"{self.node_id}: {self.name} {self.type} : { yaml.dump(self.data, width=float('inf')) if debug is True else '' }")
            for child in self.children:
                child.print(self, dag, depth + 1, callback, debug)

    def traverse(self, tree, dag=None, parent=None, depth=0, callback=None):
        dag = parent
        if callback:
            callback(tree, dag, parent, self, self.children)
        for child in self.children:
            child.traverse(tree, dag, self, depth + 1, callback)

    def clone(self):
        return copy.deepcopy(self, memo={'add_child': self.add_child, 'add_child_by_id': self.add_child_by_id,'remove_child_by_id': self.remove_child_by_id,'remove_child_by_child_id': self.remove_child_by_child_id,'print': self.print,'traverse': self.traverse})



class FileSystemTree:
    def __init__(self, template_path, dags_path, target_path, override_root=None):
        self.root = FileSystemNode("/", "root", "/")
        self.template_path = template_path
        self.dags_path = dags_path
        self.target_path = target_path
        self.jinja_env = Environment(loader=FileSystemLoader("."), variable_start_string='${',variable_end_string='}')
        if override_root is not None:
            self.root = override_root

    def clean_directory(self, path, parent_node):
        for name in os.listdir(path):
            child_path = os.path.join(path, name)
            if os.path.isdir(child_path):
                child_node = parent_node.add_child(name, child_path, type="dag")
                self.clean_directory(child_path, child_node)
            else:
                if os.path.exists(child_path) and '.out' in name:
                    os.remove(child_path)

    def scan_directory(self, path, parent_node):
        for name in os.listdir(path):
            child_path = os.path.join(path, name)
            if os.path.isdir(child_path):
                if '.out' not in name:
                    child_node = parent_node.add_child(name, child_path, type="dag")
                    self.scan_directory(child_path, child_node)
            else:
                if "METADATA" in name:
                    parent_node.update_data(utils.to_dict(child_path))
                else:
                    type = "task"
                    if ".decorator." in name:
                        type = "decorator"
                    elif ".validation." in name:
                        type = "validation"
                    elif ".template." in name:
                        type = "template"
                    else:
                        type = "task"
                    if '.out' not in name and '.yml' in name and '.validation.py' not in name:
                        parent_node.add_child(name, child_path, type=type, data=utils.to_dict(child_path))
                    elif '.out' not in name  and '.validation.py' in name:
                        parent_node.add_child(name, child_path, type=type, data={})

    def find_node_by_ids(self, parent_id, child_id):
        return self.root.find_node_by_ids(parent_id, child_id)

    def find_node_by_id(self, id):
        return self.root.find_node_by_id(id)

    def remove_child_by_child_id(self, parent_id, child_id):
        for child in self.root.children:
            if child.node_id == parent_id:
                return child.remove_child_by_child_id(child_id)
        return None

    def save_child_by_parent_id(self, parent_id, child_id, child_name, path, data, root=None, type="task"):
        root_node = self.root if root is None else root
        if root_node.node_id == parent_id:
           return root_node.save_child(child_id, child_name, path, data, type)
        else:
          for child in root_node.children:
              if child.node_id == parent_id:
                 return child.save_child(child_id, child_name, path, data, type)
              else:
                 node_found = self.save_child_by_parent_id(parent_id, child_id, child_name, path, data, child, type)
                 if node_found is not None:
                    return node_found
        return None

    def inject_child_after_by_parent_id(self, parent_id, child_id, child_name, path, data, root=None):
        root_node = self.root if root is None else root
        if root_node.node_id == parent_id:
           return root_node.inject_child_after_by_parent_id(child_id, child_name, path, data)
        else:
          for child in root_node.children:
              if child.node_id == parent_id:
                 return child.inject_child_after_by_parent_id(child_id, child_name, path, data)
              else:
                 node_found = self.inject_child_after_by_parent_id(parent_id, child_id, child_name, path, data, child)
                 if node_found is not None:
                    return node_found
        return None

    def inject_child_before_by_parent_id(self, parent_id, child_id, child_name, path, data, root=None):
        root_node = self.root if root is None else root
        if root_node.node_id == parent_id:
           return root_node.parent_node.inject_child_after_by_parent_id(child_id, child_name, path, data)
        else:
          for child in root_node.children:
              if child.node_id == parent_id:
                 return child.parent_node.inject_child_after_by_parent_id(child_id, child_name, path, data)
              else:
                 node_found = self.inject_child_before_by_parent_id(parent_id, child_id, child_name, path, data, child)
                 if node_found is not None:
                    return node_found
        return None


    def print(self, debug=False):
        print("Print Tree:" +str(debug))
        self.root.print(debug=debug)

    def traverse_file_system(self):
            print("File System:")
            self.root.traverse()

    def traverse_by_child_id(self, start_child_id, callback=None):
        for child in self.root.children:
            if child.node_id == start_child_id:
                child.traverse(callback=callback)
                break

    def traverse_by_child_id_2(self, start_child_id, root=None, callback=None):
        root = root if root is not None else self.root
        for child in root.children:
            if child.node_id == start_child_id:
                child.traverse(callback=callback)
                break
            else:
                self.traverse_by_child_id_2(start_child_id,root=child,callback=callback)

    def traverse_all_nodes(self, callback=None):
        self.root.traverse(self, callback=callback)

    def clone(self):
        return FileSystemTree(override_root=self.root.clone())
