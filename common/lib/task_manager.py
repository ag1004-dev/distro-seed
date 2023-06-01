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

def find_task_with_no_dependency(graph):
    """
    Find the Task object with no dependencies from a list of Task objects.

    Args:
        tasks (list): A list of Task objects.

    Returns:
        Task: The Task object with no dependencies.

    Raises:
        ValueError: If no task with no dependencies is found, or if multiple
        tasks with no dependencies are found.
    """
    # Initialize variables to track tasks with no dependencies
    tasks_with_no_dependencies = []
    count_no_dependencies = 0

    # Iterate over all nodes in the graph
    for node in graph.nodes():
        task = graph.nodes[node]['data']
        # Check if the task has no dependencies
        if len(task.dependencies) == 0:
            tasks_with_no_dependencies.append(node)
            count_no_dependencies += 1

    # Check the number of tasks with no dependencies
    if count_no_dependencies == 0:
        raise ValueError("No tasks found with no dependencies.")
    elif count_no_dependencies > 1:
        raise ValueError("Multiple tasks found with no dependencies.")
    else:
        return tasks_with_no_dependencies[0]

def create_rdependency_edges(graph, node):
    """
    Finds the child node in the graph that automatically adds reverse dependencies
    for the given node.

    Args:
        graph (networkx.DiGraph): A directed graph representing the task dependencies.
        node: The node to traverse to add the reverse dependencies

    Returns:
        The child next node in the graph that automatically adds reverse dependencies
    """
    auto_create_rdepends = []

    # Iterate over edges connected to the given node
    for edge in nx.edges(graph, node):
        neighbor_node = edge[1]
        neighbor_task = graph.nodes[neighbor_node]['data']
        if neighbor_task.auto_create_rdepends is True:
            auto_create_rdepends.append(neighbor_node)

    return auto_create_rdepends

def auto_add_reverse_dependencies(graph, node, rdepends_node=None):
    """
    Creates dependencies from from the children of the parent node to this node,
    unless that task also has reverse dependencies

    Args:
        graph (networkx.DiGraph): A directed graph representing the task dependencies.
        node: The node we will check any edges for and create reverse dependencies
        rdepends_node: The node representing next auto rdepends node
        If None, it will be determined automatically.

    Raises:
        ValueError: If multiple reverse dependencies are found under a single node
        during dependency creation.

    Notes:
        This method recursively creates reverse dependency edges from the
        given node to the rdepends task node. It modifies the original graph.

    """
    if rdepends_node is None:
        auto_create_rdepends = create_rdependency_edges(graph, node)
        #pprint(f'rdepends_node: {auto_create_rdepends}')
        if len(auto_create_rdepends) == 1:
            rdepends_node = auto_create_rdepends[0]
        elif len(auto_create_rdepends) > 1:
            rdepends_task_names = []
            for taskid in auto_create_rdepends:
                task = graph.nodes[taskid]['data']
                rdepends_task_names.append(f'{task.config}:{task.cmd}')
            raise ValueError(f'Error: Multiple forced dependency tasks found {rdepends_task_names}')
        else:
            return

    for edge in graph.edges(node):
        if edge[1] != rdepends_node:
            #pprint(f'edge: {edge[1]}')
            #pprint(f'rdepends_node: {rdepends_node}')
            graph.add_edge(edge[1], rdepends_node, label="auto_added_dep")
            auto_add_reverse_dependencies(graph, edge[1], rdepends_node)

    auto_add_reverse_dependencies(graph, rdepends_node, None)

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
                    label = ''
                    if task.auto_create_rdepends:
                        label = 'auto_rdepends_task'
                    graph.add_edge(subtask.id, task.id, label=label)
                    found = 1
            if found == 0:
                raise ValueError (f'Unsatisifed dependency {dep} from {task.config}')

    first_task_id = find_task_with_no_dependency(graph)

    # Recurseively traverse all nodes and creat edges for auto_create_rdepends
    auto_add_reverse_dependencies(graph, first_task_id, None)

    return graph

def print_deps(tasks, nodename=None):
    graph = create_task_graph(tasks)
    normal_edges = [(u, v) for (u, v, d) in graph.edges(data=True)
                    if d['label'] == '']
    flush_task_edges = [(u, v) for (u, v, d) in graph.edges(data=True)
                        if d['label'] == 'auto_rdepends_task']
    flush_dep_edges = [(u, v) for (u, v, d) in graph.edges(data=True)
                        if d['label'] == 'auto_added_dep']

    pos = nx.nx_pydot.pydot_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_size=400)
    nx.draw_networkx_edges(graph, pos, edgelist=flush_task_edges, width=2)
    nx.draw_networkx_edges(graph, pos, edgelist=normal_edges, width=2,
                            alpha=0.5, edge_color="blue", style="dashed")
    nx.draw_networkx_edges(graph, pos, edgelist=flush_dep_edges, width=2,
                            alpha=0.5, edge_color="green", style="dashed")

    node_labels = {}
    for task in tasks:

        node_labels[task.id] = f'{task.id}:{task.config}'

        if len(task.provides) > 0:
            node_labels[task.id] += f'/{task.provides}'
        
        if len(task.cmd) > 0:
            node_labels[task.id] += f' ({task.cmd})'
    nx.draw_networkx_labels(graph, pos, font_size=10, font_family="sans-serif",
                            labels=node_labels)
    #edge_labels = nx.get_edge_attributes(graph, 'label')
    #nx.draw_networkx_edge_labels(graph, pos, edge_labels)
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
