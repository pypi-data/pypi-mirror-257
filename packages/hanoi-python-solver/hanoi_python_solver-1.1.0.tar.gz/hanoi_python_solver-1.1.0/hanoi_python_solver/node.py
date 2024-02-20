import functools
from types import NotImplementedType


@functools.total_ordering
class Node:
    """A node/vertex in a Network (a string label and a float weight)
    """
    def __init__(self, node_id:str, node_weight:float) -> None:
        self._node_id:str = node_id
        self._weight:float = node_weight        

    @property
    def id(self) -> str:
        return self._node_id
    
    @property
    def weight(self) -> float:
        return self._weight
    
    @weight.setter
    def weight(self, new_weight:float) -> None:
        self._weight = new_weight
        
    # in order to be compared in the heapq, Node must be compared to an other Node
    # So we have to define the "equal" operator for a Node
    def __eq__(self, other:object) -> NotImplementedType | bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.weight == other.weight

    # in order to be compared in the heapq, Node must be compared to an other Node
    # So we have to define the "less than" operator for a Node
    def __lt__(self, other:object) -> NotImplementedType | bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.weight < other.weight

    
    def __str__(self) -> str:
        return f'N{self._node_id}({self._weight})'