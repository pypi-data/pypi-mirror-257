'''
This is a common interface to KV stores for the swarm space.

Things like action, util and memory space metadata, swarm state, 
swarm history and more will be stored in KV stores.
'''
from __future__ import annotations
from typing import TYPE_CHECKING
from importlib import import_module

if TYPE_CHECKING:
    from tree_swarm.swarm.types.swarm_config import Swarm
    

platform_map = {
    'mac': 'tree_swarm.utils.data.kv_operations.mongodb',
    'azure': 'tree_swarm.utils.data.kv_operations.cosmos_db',
}

def add_kv(swarm: Swarm, category: str, key: str, value: dict) -> None:
    platform = swarm.platform
    kv_operations_module = import_module(platform_map[platform])
    return kv_operations_module.add_kv(swarm, category, key, value)

def get_kv(swarm: Swarm, category: str, key: str) -> dict:
    platform = swarm.platform
    kv_operations_module = import_module(platform_map[platform])
    return kv_operations_module.get_kv(swarm, category, key)

def delete_kv(swarm: Swarm, category: str, key: str) -> None:
    platform = swarm.platform
    kv_operations_module = import_module(platform_map[platform])
    return kv_operations_module.delete_swarm_space_kv_document(swarm, category, key)

def update_kv(swarm: Swarm, category: str, key: str, value: dict) -> None:
    platform = swarm.platform
    kv_operations_module = import_module(platform_map[platform])
    return kv_operations_module.update_kv(swarm, category, key, value)
