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
        enforce_dependencies (bool): Flag indicating whether to enforce task dependencies.
    """
    cmd_type: str
    cmd: str
    dependencies: List[str]
    provides: str
    description: str
    enforce_dependencies: bool
