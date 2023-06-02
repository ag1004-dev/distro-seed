import os
from typing import List
from pprint import pprint

import yaml
import networkx as nx
import matplotlib.pyplot as plt

from lib.task_manifest import TaskManifest
from lib.task import Task

def load_tasks_from_manifest(manifest_file):
    """
    Returns a list tasks from a single manifest filew
    """
    manifest_path = os.path.dirname(manifest_file)

    tasks = []

    with open(manifest_file, 'r', encoding='utf-8') as f:
        manifest_data = yaml.safe_load(f)
        config = manifest_data['config']

        for task_data in manifest_data['tasks']:
            task_config = TaskManifest(
                cmd_type = task_data['cmd_type'],
                cmd = task_data.get('cmd', ""),
                dependencies = task_data.get('dependencies', []),
                provides = task_data.get('provides', ""),
                description = task_data['description'],
                auto_create_rdepends = task_data.get('auto_create_rdepends', False)
            )
            if task_config.cmd_type not in ['host', 'docker', 'target', 'dummy']:
                raise ValueError(f"Invalid task type '{task_config.cmd_type}' "
                                    f"in manifest file '{manifest_file}'")
            tasks.append(Task(config, manifest_path, task_config))

    return tasks

def get_task_by_id(tasks, id):
    """
    Retrieves a task from a list of tasks based on its ID.

    Args:
        tasks (list): A list of tasks.
        id: The ID of the task to retrieve.

    Returns:
        The task object with the specified ID.

    Raises:
        ValueError: If the task with the specified ID is not found.
    """
    for task in tasks:
        if task.id == id:
            return task
    raise ValueError(f"Task with ID {id} not found.")

def sort_generation(generation, tasks):
    """
    Sorts a generation of task IDs within a generation by their number. This
    keeps the ordering within a manifest for any tasks otherwise with the
    same dependencies

    Args:
        generation (list): A list of task IDs representing a generation.
        tasks (list): A list of task objects containing the task configurations.

    Returns:
        list: A sorted generation of task IDs

    """
    sorted_generation = sorted(generation,
                                key=lambda genid: get_task_by_id(tasks, genid).config)
    return sorted_generation

def topological_sort(graph, tasks):
    """
    Performs a topological sort on a graph of tasks and yields each sorted generation.

    Args:
        graph (networkx.DiGraph): A directed graph representing the task dependencies.
        tasks (list): A list of task objects containing the task configurations.

    Yields:
        list: A sorted generation of task IDs based on the task configuration.

    """
    for generation in nx.topological_generations(graph):
        sorted_generation = sort_generation(generation, tasks)
        yield from sorted_generation

def add_edge_to_parent(graph, node):
    """
    Add an edge in the graph from the given node to a child node derived from its parents.

    This function performs a breadth-first search from each parent node of the given node,
    and then it selects the first child node whose associated task has the 'auto_create_rdepends'
    attribute set to True.

    If such a child node is found, an edge is added in the graph from the given node to the
    selected child node.

    Args:
        graph (nx.DiGraph): A directed graph where nodes represent tasks and edges represent
        dependencies between tasks.

        node (nx.Node): Node in the graph to BFS search from

    """
    # Find all parents of the node
    parents = [n for n, d in graph.in_edges(node)]

    # Perform BFS from each parent and get all edges
    all_edges = []
    for parent_node in parents:
        all_edges.extend(list(nx.edge_bfs(graph, parent_node)))

    # Iterate over the edges until we find one that meets the conditions
    child = None
    for edge in all_edges:
        task = graph.nodes[edge[1]]['data']
        if task.auto_create_rdepends is True:
            child = edge[1]
            break

    if child is not None:
        graph.add_edge(node, child, label='auto_added_dep')

def create_task_graph(tasks):
    """
    Creates a networkx.DiGraph representing the tasks and their dependencies.

    Args:
        A list of Task objects to convert to a graph

    Raises:
        ValueError: If there are unsatisfied depenedencies in the tasks
    """
    graph = nx.DiGraph()

    # Add nodes for each task
    # We attach an id to each task in the order we read it in.
    # This way if there are no other order priorities, the tasks are
    # sorted the way they are listed in the manifest.
    for i, task in enumerate(tasks, start=1):
        task.id = i
        graph.add_node(task.id, data=task)

    # Create edges for each dependency to each config or provides
    for task in tasks:
        for dep in task.dependencies:
            found = 0
            for subtask in tasks:
                if subtask.config == dep or subtask.provides == dep:
                    graph.add_edge(subtask.id, task.id, label='')
                    found = 1
            if found == 0:
                raise ValueError (f'Unsatisifed dependency {dep} from {task.config}')

    # Recurseively traverse all nodes and create edges for auto_create_rdepends
    for node in graph.nodes:
        if not graph.out_degree(node):
            add_edge_to_parent(graph, node)

    return graph

def print_deps(tasks):
    """
    Creates a matplotlib drawing of the tasks list
    """
    graph = create_task_graph(tasks)
    normal_edges = [(u, v) for (u, v, d) in graph.edges(data=True)
                    if d['label'] == '']
    flush_dep_edges = [(u, v) for (u, v, d) in graph.edges(data=True)
                        if d['label'] == 'auto_added_dep']

    pos = nx.nx_pydot.pydot_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_size=400)
    nx.draw_networkx_edges(graph, pos, edgelist=normal_edges, width=2)
    nx.draw_networkx_edges(graph, pos, edgelist=flush_dep_edges, width=2,
                            alpha=0.5, edge_color="green", style="dashed")

    node_labels = {}
    for task in tasks:

        node_labels[task.id] = f'{task.id}:{task.config}'

        if len(task.provides) > 0:
            node_labels[task.id] += f'/{task.provides}'
        if len(task.cmd) > 0:
            node_labels[task.id] += f' ({task.cmd})'
        if task.auto_create_rdepends is True:
            node_labels[task.id] += '(rdeps)'
    nx.draw_networkx_labels(graph, pos, font_size=10, font_family="sans-serif",
                            labels=node_labels)
    plot_axis = plt.gca()
    plot_axis.margins(0.00)
    plt.axis("off")
    plt.tight_layout()

    plt.show()

def sort(tasks):
    """
    Sorts a list of tasks based on their dependencies.

    Args:
        tasks (list): A list of task objects representing the tasks to be sorted.
        print_deps (bool): A flag indicating whether to print the task 
        dependencies during sorting.

    Returns:
        list: A sorted list of tasks based on their dependencies.

    """
    graph = create_task_graph(tasks)
    sorted_ids = [id for id in topological_sort(graph, tasks)]
    sorted_tasks = sorted(tasks, key=lambda task: sorted_ids.index(task.id))

    # Now that we have an authoratative order, we re rewrite the ids with the actual order
    # this is used for overlays so they get combined in order
    for i, task in enumerate(tasks, start=1):
        task.id = i

    return sorted_tasks
