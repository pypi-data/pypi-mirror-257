'''
This is a common interface for file operations for the swarm space.

All file operations will happen within the swarm space root path.
'''
from __future__ import annotations
from typing import TYPE_CHECKING
from importlib import import_module

from tree_swarm.utils.data.paths import validate_and_adjust_swarm_space_path

if TYPE_CHECKING:
    from tree_swarm.swarm.types import Swarm

platform_map = {
    'mac': 'aga_swarm.utils.data.file_operations.local_storage',
    'azure': 'aga_swarm.utils.data.file_operations.azure_blob_storage',
}

def delete_swarm_space_file(swarm: Swarm, file_path: str) -> None:
    platform = swarm.platform.value
    file_path = validate_and_adjust_swarm_space_path(file_path, swarm.swarm_space_root_path)
    file_operations_module = import_module(platform_map[platform])
    return file_operations_module.delete_file(swarm, file_path)

def move_swarm_space_file(swarm: Swarm, file_path: str, new_file_path: str) -> None:
    platform = swarm.platform.value
    file_path = validate_and_adjust_swarm_space_path(file_path, swarm.swarm_space_root_path)
    new_file_path = validate_and_adjust_swarm_space_path(new_file_path, swarm.swarm_space_root_path)
    file_operations_module = import_module(platform_map[platform])
    return file_operations_module.move_file(swarm, file_path, new_file_path)

def rename_swarm_space_file(swarm: Swarm, file_path: str, new_file_name: str) -> None:
    platform = swarm.platform.value
    file_path = validate_and_adjust_swarm_space_path(file_path, swarm.swarm_space_root_path)
    new_file_name = validate_and_adjust_swarm_space_path(new_file_name, swarm.swarm_space_root_path)
    file_operations_module = import_module(platform_map[platform])
    return file_operations_module.rename_file(swarm, file_path, new_file_name)

def upload_swarm_space_file(swarm: Swarm, file_path: str, file_bytes: bytes) -> None:
    platform = swarm.platform.value
    file_path = validate_and_adjust_swarm_space_path(file_path, swarm.swarm_space_root_path)
    file_operations_module = import_module(platform_map[platform])
    return file_operations_module.upload_file(swarm, file_path, file_bytes)

def retrieve_swarm_space_file(swarm: Swarm, file_path: str) -> bytes:
    platform = swarm.platform.value
    file_path = validate_and_adjust_swarm_space_path(file_path, swarm.swarm_space_root_path)
    file_operations_module = import_module(platform_map[platform])
    return file_operations_module.retrieve_file(swarm, file_path)
