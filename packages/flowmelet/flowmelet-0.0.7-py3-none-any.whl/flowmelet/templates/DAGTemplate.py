{%- for import in imports -%}
{{ import }}
{% endfor %}

dag = DAG('{{ dag_name }}',{% for dag_param in dag_params %}{{ dag_param }},{% endfor %})

{% for task in tasks -%}
{% if 'python_callable' in task %}
{{task['python_callable']}}
{% endif -%}
{{task['id']}} = {{task['operator']}}(task_id='{{task['id']}}',{% for operator_param in task['operator_params'] %}{{ operator_param }},{% endfor %} dag=dag)
{% endfor %}

{% for vertix in vertices -%}
{{ vertix['A'] }} >> {{ vertix['B'] }}
{% endfor %}