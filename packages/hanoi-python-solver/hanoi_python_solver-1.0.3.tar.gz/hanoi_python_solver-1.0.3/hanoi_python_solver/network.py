import heapq
import sys
from typing import Dict, List, Tuple
from node import Node


class Network:
    """
        This class implements a non oriented, non multigraph, graph
        with vertices (also called nodes) and edges.
    
        Nodes and edges are weighed. Network is not suitable 
        when you need to remove edges or nodes.
    """
    def __init__(self) -> None:
        self.edges:Dict[str,List[Tuple[str,float]]] = {}
        self.nodes:Dict[str,Node] = {}
        self.neighbors:Dict[str,List[Tuple[Node,float]]] = {}
        
    @classmethod
    def fromAdjacencyMatrix(cls, file_name:str):
        """
        Reads an adjacency matrix placed in a text file. 1st line contains 0 and node names
        separated by space character. All the other lines begin with the name of the node
        followed by 0 (if there's no edge between this node and the given one) or the weight

        Args:
            file_name (str): file name

        Returns:
            Network | None : the Network created from the file content or None if an error occured.
        """
        try:
            f = open(file_name)
        except FileNotFoundError as e:
            print(f"{file_name} not found : {e.args}")
            return None

        lines = f.readlines()
        f.close()
        
        if len(lines) == 0:
            return None
        
        retour = Network()
        
        count = 0
        node_names:List[str] = []
        
        for l in lines:
            s = l.strip().split(' ')
            if count == 0:
                # reading the header of the file
                # s contains names of nodes
                for i in range(1, len(s)):
                    node_names.append(s[i])
            else:
                # s contains different edges from the current node in s[0]
                start_node = s[0]
                for i in range(1, len(s) - 1):
                    val = s[i]
                    if val != "0":
                        end_node = node_names[i-1]
                        retour.add_edge(start_node,end_node,float(val))
            count += 1
            
        return retour
        
    
    def edge_list_size(self) -> int:
        taille = 0;
        for _key, edge_list in self.edges.items():
            comb = len(edge_list)
            taille += comb
        return taille

    @property
    def nodes_list_size(self) -> int:
        return len(self.nodes)
    
    def changeWeight(self, node_id:str, new_value:float) -> float|None:
        """changes the weight of the given node and returs the old value
        (or None if the given node doesn't exist)

        Args:
            node_id (str): node id 
            new_value (float): the new weight value to set to the node

        Returns:
            float: old value or None if node_id doesn't exist
        """
        the_node = self.nodes.get(node_id)
        if the_node == None:
            return None
        ret = the_node.weight
        the_node.weight = new_value
        return ret
 
 
    def containsNode(self, node_id:str)->bool:
        return self.nodes.get(node_id) != None
          

    def add_edge(self,start_node:str, end_node:str, label:float = 1.0) -> int:
        """
        Adds an edge to this Network using the two given vertices and a label. If 
        both or one vertex do not already exist, they are automatically added.
        
        Network is not a multigraph : there cannot be two edges between two same nodes.
        
        When adding an edge, the Network's neighbors list will be updated at the same time.

        Args:
            start_node:  start node for the edge
            end_node:  end node for the edge
            label:  length or weight of edge
            
        Returns:
            0 : nothing was done
            1 : edge was added
            2 : edge and 1 node were added
            3 : two nodes and 1 edge were added.
        """
        counter = 0
        idx_st = self.nodes.get(start_node)
        if idx_st == None:
            new_n:Node = Node(start_node, 1.0)
            self.nodes[start_node] = new_n
            counter += 1
            idx_st = new_n
        
        idx_end = self.nodes.get(end_node)
        if idx_end == None:
            new_n:Node = Node(end_node, 1.0)
            self.nodes[end_node] = new_n
            counter += 1
            idx_end = new_n

        " So far, nodes are created. Let's see the edges dictionnary"
        idx_edge = self.edges.get(start_node)
        if idx_edge == None:
            idx_edge = self.edges.get(end_node)
            if idx_edge == None:
                "there's no entry in edges for start or end node : add a new edge"
                counter += 1
                self.edges[start_node] = [(end_node, float(label))]
                self._addNeighbor(idx_st, idx_end, float(label))
            else:
                found = False
                for x in idx_edge:
                    if x[0] == start_node:
                        found = True
                        break;
                if not found:
                    "edge between end and start doesn't exist : so add it"
                    counter += 1
                    idx_edge.append((start_node,float(label)))
                    self._addNeighbor(idx_st, idx_end, float(label))
        else:
            "an edge starting from start node already exists : check if end node is already in the list"
            found = False
            for x in idx_edge:
                if x[0] == end_node:
                    found = True
                    break;
            if not found:
                counter += 1
                idx_edge.append((end_node,float(label)))
                self._addNeighbor(idx_st, idx_end, float(label))
        return counter
    
    
    def _addNeighbor(self, start:Node, end:Node, edge_weight:float) -> None:
        """Adds end to the neighbors list of start (if not 
        already present). As this Network is not oriented, also adds start 
        to the neighbors list of end.
        
        If an edge between start and end exists, the existing weight will not
        be replace with the given weight.

        Args:
            start (Node): the node to which we want to add end node as a neighbor
            end (Node): the neighbor to add to start node id
        """
        # check if start has neighbors
        entry = self.neighbors.get(start.id)
        if entry == None:
            # create a new list with end node id
            self.neighbors[start.id] = [(end, edge_weight)]
        else:
            # search the existing list if end is already in the list
            found = False
            for t in entry:
                if t[0].id == end.id:
                    found = True
                    break;
            if not found:
                entry.append((end, edge_weight))
                
        # let's do the same for end->start
        entry = self.neighbors.get(end.id)
        if entry == None:
            # create a new list with start node id
            self.neighbors[end.id] = [(start, edge_weight)]
        else:
            # search the existing list if end is already in the list
            found = False
            for t in entry:
                if t[0].id == start.id:
                    found = True
                    break;
            if not found:
                entry.append((start, edge_weight))
        
    def DOT_description(self) -> str:
        """
        Generates the description of this Network in DOT language, 
        allowing you to easily get a graphical representation
        of the graph (example on https://edotor.net/)

        Returns:
            str: this Network in DOT language
        """
        ret:List[str] = ["graph {","node [style=filled]"]
        for k, liste in self.edges.items():
            dep_node = self.nodes.get(k)
            if dep_node != None:                
                dep_node_DOT = f'\"{dep_node.id}({dep_node.weight})\"'
                #ret.append(dep_node_DOT)
                for t in liste:
                    arr_node = self.nodes.get(t[0])
                    if arr_node != None:
                        arr_node_DOT = f'\"{arr_node.id}({arr_node.weight})\"'
                        #ret.append(arr_node_DOT)
                        ret.append(f"{dep_node_DOT}--{arr_node_DOT}   [label=\"{t[1]}\"]")
        ret.append("}")
        return '\n'.join(ret)
            
        
    def dijkstra(self, start_id:str, end_id:str) -> Dict[str,List[str]]:
        """
        Implementation of Dijkstra's shortest path algorithm with a MinHeap 
        so that to efficiently order the nodes.

        Args:
            start_id (str): id of the start node
            end_id (str): id of the end node

        Returns:
            a dictionnary with two entries
            - "path" : the shortest path from start to end node
            - "prec" : couples of strings (the node and its best predecessor) 
            for all the nodes and placed one after the other in the returned list
        """
        # variables that will be returned by this method
        predecessors:Dict[str,Tuple[Node, Node | None]] = {}
        # Dijkstra's algorithm initialisation
        self._store_infinity(self.nodes)
        self.changeWeight(start_id, 0.0)
        # create a priority queue and get the start node with the given id
        queue:List[Tuple[float,Node]] = []
        current_node = self.nodes.get(start_id)
        # check if start id is known !
        if current_node == None:
            ret:Dict[str,List[str]] = {
                "path" : [f"no path found : start id {start_id} doesn't exist in the Network"],
                "prec" : ["no predecessors found"]
            }
            return ret
        # mark start node with no predecessor
        predecessors[start_id] = (current_node , None)
        # put the departure node in a priority queue
        heapq.heappush(queue, (current_node.weight , current_node)) # in O(n lon(n))
        # begin Dijkstra's algorithm
        while len(queue) > 0:
            # extract the best node from our priority queue 
            # ie, the one with the lowest weight or shortest path !!
            current_node = heapq.heappop(queue)  # access in O(ln (n))
            departure_node_weight = current_node[0]
            # search all neighbors of the current node and determine the new weight of these neighbors
            voisins = self.neighbors.get(current_node[1].id)
            if voisins != None:
                for dest_node in voisins:
                    # determine new weight of destination node with current weight of
                    # departure node and edge weight
                    dest_node_weight = dest_node[0].weight;
                    edge_weight = dest_node[1];
                    new_dest_node_weight = departure_node_weight + edge_weight
                    best_path = new_dest_node_weight < dest_node_weight
                    if best_path:
                        # 1/ change the weight of dest node
                        # 2/ push dest node in the priority queue because we have a new best value
                        # 3/ remember that departure node is predecessor of dest node
                        dest_node[0].weight = new_dest_node_weight
                        heapq.heappush(queue, (dest_node[0].weight , dest_node[0]))
                        predecessors[dest_node[0].id] = (dest_node[0] , current_node[1])
            
        # Dijkstra ends here with two variables :
        #  - first we have a list of best predecessors for each node in the Network
        #  - we have the minimum weight for all the nodes in the Network
            
        # now we just need to find the path from start to end node
        path = self._getPath(end_id, predecessors)
        prec = self._printPredecessors(predecessors)
        return {
            "path": path,
            "prec": prec
            }
        
        
    def _printPredecessors(self, predecessors:Dict[str,Tuple[Node, Node | None]]) -> List[str]:
        ret:List[str] = []
        for _k, t in predecessors.items():
            end_id = t[0].id
            if(t[1] == None):
                start_id = "None"
            else:
                start_id = t[1].id
            ret.append(end_id)
            ret.append(start_id)
        return ret
            
    
    
    def _getPath(self, end_id:str, predecessors:Dict[str,Tuple[Node, Node | None]]) -> List[str]:
        current_node = self.nodes.get(end_id)
        ret:str = "End node not found in this Network"
        if current_node != None:
            ret = f"{end_id}({current_node.weight})"
            pred = predecessors.get(current_node.id)
            while pred != None:
                predecesseur = pred[1];
                if(predecesseur != None):
                    ret = f'{predecesseur.id}({predecesseur.weight}) - ' + ret
                    pred = predecessors.get(predecesseur.id)
                else:
                    pred = None
        return [ret]


    def _store_infinity(self, nodes:Dict[str, Node]) -> None:
        """
        Sets the weight of all nodes in this Network at the positive
        infinity value

        Args:
            nodes (Dict[str, Node]): the Network nodes dict
        """
        for _k,v in nodes.items():
            v.weight = sys.float_info.max
            
    