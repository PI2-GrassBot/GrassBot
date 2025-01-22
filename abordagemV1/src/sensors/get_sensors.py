from core.node import Node
from typing import List

def get_sensors(node: Node) -> List[Node]:
    node_positions = [(node.position[0] + new_pos[0],
                       node.position[1] + new_pos[1])
                       for new_pos in [(-1, 0), (0, 1), (1, 0), (0, -1)]]
    neighbors = [Node(node, node_pos) for node_pos in node_positions]
    return neighbors

def is_neighbor(current_node: Node, next_node: Node):
    if abs(current_node.position[0] - next_node.position[0]) > 1 \
    or abs(current_node.position[1] - next_node.position[1]) > 1:
        return False
    return True
