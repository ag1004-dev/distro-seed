from typing import List
from dataclasses import dataclass

@dataclass
class TaskManifest:
    """
    Configuration class for defining a task.

    Attributes:
        cmd_type (str): The type of the command. (host/docker/target)
        cmd (str): path to the script to run
        dependencies (List[str]): List of task dependencies.
        provides (str): The output provided by the task.
        description (str): Description of the task.
        auto_create_rdepends (bool): Flag indicating whether to automatically 
                                     create reverse dependencies from the parent node
    """
    cmd_type: str
    cmd: str
    dependencies: List[str]
    provides: str
    description: str
    auto_create_rdepends: bool
