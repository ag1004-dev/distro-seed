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
            if task_config.cmd_type not in ['host', 'docker', 'target', 'dummy', 'packagelist']:
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

def find_edge_to_parent(graph, node):
    """
    This function finds and returns a tuple of nodes (parent, child) in the given directed
    graph where the child has auto_create_rdepends set to True.
    The function starts by examining the predecessors of the specified node in the graph,
    and checks their successors. If no such child is found, the function emits a warning
    and returns None.

    Parameters:
    graph (nx.DiGraph): The graph to analyze.
    node: The node to find an edge to its parent.

    Returns:
    tuple or None: A tuple (parent, child) if a suitable child is found, or None otherwise.
    """
    queue = list(graph.predecessors(node))
    node_task = graph.nodes[node]['data']
    #print(f"\nTask: {node_task.config}")
    child = None
    found_child = False
    while queue and not found_child:
        current_node = queue.pop(0)
        current_task = graph.nodes[current_node]['data']
        #print(f"Checking parent: {current_task.config}")
        for child_node in graph.successors(current_node):
            if child_node == node or child_node in graph.predecessors(node):
                continue
            child_task = graph.nodes[child_node]['data']
            #print(f"Checking child: {child_task.config}")
            if child_task.auto_create_rdepends is True:
                child = child_node
                #print(f"Adding edge to: {child_task.config}")
                found_child = True
                break
        if not found_child:
            queue.extend(graph.predecessors(current_node))
    if child is not None:
        return (node, child)
    else:
        task = graph.nodes[node]['data']
        #print(f"Warning: No child with auto_create_rdepends=True found for node {task.config}")
        return None

def create_task_graph(tasks):
    """
    This function adds all edges at once after the loop that calls add_edge_to_parent.
    """
    graph = nx.DiGraph()
    for i, task in enumerate(tasks, start=1):
        task.id = i
        graph.add_node(task.id, data=task)
    for task in tasks:
        for dep in task.dependencies:
            found = 0
            for subtask in tasks:
                if subtask.config == dep or subtask.provides == dep:
                    graph.add_edge(subtask.id, task.id, label='')
                    found = 1
            if found == 0:
                raise ValueError (f'Unsatisifed dependency {dep} from {task.config}')

    # Collect all edges that need to be added
    edges_to_add = []
    for node in graph.nodes:
        if not graph.out_degree(node):
            task = graph.nodes[node]['data']
            if task.auto_create_rdepends is False:
                edge = find_edge_to_parent(graph, node)
                if edge is not None:
                    edges_to_add.append(edge)

    # Add all edges at once
    for edge in edges_to_add:
        graph.add_edge(*edge, label='auto_added_dep')

    return graph

def detect_cycles(graph):
    """
    This function detects any cycles present in a directed graph.

    A cycle in a graph represents a situation where a node can be reached from
    itself following the graph's edges. In this case, it indicates a dependency
    loop. If any cycles are detected, it raises a ValueError indicating invalid dependencies.

    Parameters:
    graph (nx.DiGraph): The graph to analyze for cycles.

    Returns:
    None.

    Raises:
    ValueError: If a cycle is found in the graph, indicating invalid dependencies.
    """
    cycles = list(nx.simple_cycles(graph))
    if cycles:
        print("Found a dependency loop!")
        for cycle in cycles:
            for node in cycle:
                current_task = graph.nodes[node]['data']
                print(f"    {current_task.config}")
        raise ValueError ('Invalid dependencies')

def print_deps(tasks):
    """
    Creates a matplotlib drawing of the tasks list
    """
    graph = create_task_graph(tasks)
    detect_cycles(graph)
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
    detect_cycles(graph)
    sorted_ids = [id for id in topological_sort(graph, tasks)]
    sorted_tasks = sorted(tasks, key=lambda task: sorted_ids.index(task.id))

    # Now that we have an authoratative order, we re rewrite the ids with the actual order
    # this is used for overlays so they get combined in order
    for i, task in enumerate(tasks, start=1):
        task.id = i

    return sorted_tasks
