import typing
import dagfactory
import yaml
from yaml import SafeLoader

DAG_CONFIG = """
{{dag_yml}}
"""

dag_factory = dagfactory.DagFactory(config=yaml.load(DAG_CONFIG, Loader=SafeLoader))

dag_factory.clean_dags(globals())
dag_factory.generate_dags(globals())


