'''
The swarm state is a record of the current state of the swarm. It
simply stores a dictionary of all nodes. This state can be deconstructed
and reconstructed from the history.
'''
from pydantic import BaseModel

from tree_swarm.utils.data.kv_operations.main import get_kv, add_kv
from tree_swarm.swarm.types.swarm_config import SwarmConfig
from tree_swarm.swarm.types.swarm import SwarmNode

class SwarmState(BaseModel):
    swarm: SwarmConfig
    
    def __getitem__(self, node_id: str) -> SwarmNode:
        node = SwarmNode.model_validate(get_kv(self.swarm, 'swarm_state', node_id))
        return node
        
    def update_state(self, node: SwarmNode):
        add_kv(self.swarm, 'swarm_state', node.node_id, node.model_dump_json())
    