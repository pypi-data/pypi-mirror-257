from typing import List, Tuple
from hanoi_python_solver.network import Network

from hanoi_python_solver.poteau import Poteau


class Hanoi:
    """
    A class that implements a Tower of Hanoi game, with THREE rods and any given 
    number of disks (max is currently 10). Allows you to move and get an ABC string
    for the current position of disks. Get all the possible moves at each step.
    
    Also allows you to find the shortest path to the solution !!

    Raises:
        ValueError: in the constructor, if the given number of disks exceeds 
        the max number (10)

    """
    max_disk_number = 10
    
    def __init__(self, nb_disks:int) -> None:
        """
        Instancies a new Hanoi class with all disks slid on the first rod.

        Args:
            nb_disks (int): how many disks in this new game ?

        Raises:
            ValueError: if the given number of disks is greater than max number (10)
        """
        if nb_disks > self.max_disk_number:
            raise ValueError(f"cannot create a Hanoi with {nb_disks} disks (max = {self.max_disk_number})")
        self._p:List[Poteau] = []
        start_position:str = "A" * nb_disks
        self._nb_disks = nb_disks
        self._p.append(Poteau.createFromABC(start_position,1))
        self._p.append(Poteau.createFromABC(start_position,2))
        self._p.append(Poteau.createFromABC(start_position,3))
        
    def __str__(self) -> str:
        p1 = self._p[0].getDisks()
        p2 = self._p[1].getDisks()
        p3 = self._p[2].getDisks()
        return f"{p1}-{p2}-{p3}"
        
    def getABC(self) -> str:
        ret:List[str] = []
        p1 = self._p[0].getDisks()
        p2 = self._p[1].getDisks()
        p3 = self._p[2].getDisks()
        for i in range(self._nb_disks + 1 , 0 , -1):
            try:
                p1.index(i)
            except:
                # ignore exception and go to next poteau
                pass
            else:
                ret.append("A")
            try:
                p2.index(i)
            except:
                # ignore exception and go to next poteau
                pass
            else:
                ret.append("B")
            try:
                p3.index(i)
            except:
                # ignore exception and go to next poteau
                pass
            else:
                ret.append("C")
        
        return ''.join(ret)
    
    def move(self, t:Tuple[int, int] ) -> bool:
        """
        Moves (if possible) from the fisrt poteau given in the tuple to the second.

        Args:
            t (Tuple[int, int]): a tuple of poteau number. ie : (1,2) to move
            from Poteau 1 to Poteau 2

        Returns:
            bool: True if the move was possible, False otherwise
        """
        p1 = self._p[t[0] - 1]
        p2 = self._p[t[1] - 1]
        resu = p1.moveTo(p2)
        return resu
    
    def possibleMoves(self) -> List[Tuple[int,int]]:
        """
        Gets all the possible move from the current position. Generally, 
        there are 3 possible moves. But if all the disks are stacked on
        one rod, there are only 2 possible moves.

        Returns:
            List[Tuple[int,int]]: a list of all possible moves (a move is a tuple)
        """
        p1 = self._p[0]
        p2 = self._p[1]
        p3 = self._p[2]
        ret:List[Tuple[int,int]] = []
        if p1.checkMove(p2):
            ret.append((1,2))
        if p2.checkMove(p1):
            ret.append((2,1))
        if p1.checkMove(p3):
            ret.append((1,3))
        if p3.checkMove(p1):
            ret.append((3,1))
        if p2.checkMove(p3):
            ret.append((2,3))
        if p3.checkMove(p2):
            ret.append((3,2))
        return ret
    
    def pathToSolution(self, solution:str) -> str:
        # _graph stores the graph of all positions for this TOH game
        try:
            self._graph
        except:
            # NameError exception occurs if _graph is not initialized
            # so, let's initialize it !
            g:Network = Hanoi._constructGraph(self._nb_disks)
            self._graph = g
        print(self._graph.DOT_description())
        start_pos = self.getABC()
        result = self._graph.dijkstra(start_pos,solution)
        path = result["path"]
        return path[0]
    
    @property
    def getPoteau1(self) -> Poteau:
        return self._p[0]

    @property
    def getPoteau2(self) -> Poteau:
        return self._p[1]
    
    @property
    def getPoteau3(self) -> Poteau:
        return self._p[2]

    @property
    def nbDisks(self) -> int:
        return self._nb_disks

    
    @classmethod  
    def _constructGraph(cls, nb_disks:int) -> Network:
        h = Hanoi(nb_disks)
        g = Network()
        h._discoverPositions(h.getPoteau1, h.getPoteau3, h.getPoteau2, g, nb_disks)
        return g

    def _discoverPositions(self,source:Poteau, dest:Poteau, inter:Poteau, graphe:Network, nb_disques:int) -> None:
        """
        Recursive method that explores all possible position of a Tower of Hanoi game with the 
        given disks. Constructs the graph of all positions that can later be used to find a path
        to the solution from any position in the game.

        Args:
            source (Poteau): the source rod
            dest (Poteau): the destination rod
            inter (Poteau): the third rod is the intermediary
            graphe (Network): a graph containing all ABC strings reachable in a TOH game
            nb_disques (int): how many disks to move
        """
        if nb_disques == 1:
            ## to find all possible positions with 1 disk, we will move 
            # from 1 to 2,then from 2 to 3 and then from 3 to 1
            
            # source -> intermédiaire
            s_depart = self.getABC()
            source.moveTo(inter)
            s_inter = self.getABC()
            graphe.add_edge(s_depart , s_inter)
            
            # inter -> dest
            inter.moveTo(dest)
            s_arrivee = self.getABC()
            graphe.add_edge(s_inter , s_arrivee)
            
            # dest -> source
            graphe.add_edge(s_arrivee , s_depart)
            
            ## the following permits to add edges that the recursion doesn't find
            fins_en_CB = [
                "CB",
                "CBB",
                "CBBB",
                "CBBBB",
                "CBBBBB",
                "CBBBBBB",
                "CBBBBBBB",
                "CBBBBBBBB",
                "CBBBBBBBBB",
                "CBBBBBBBBBB",
            ]
            for fin_cb in fins_en_CB:
                if s_inter.endswith(fin_cb):
                    # this part of algo does the subsitution 
                    # from X..XCB..B to X..XAB..B 
                    # and add an edge between these two ABC notations
                    fin_l = len(fin_cb)
                    longueur = len(s_inter) - fin_l
                    fin_ab = "A" + fin_cb[1:]
                    if longueur >= 0:
                        s_ab = s_inter[0:longueur] + fin_ab
                        graphe.add_edge(s_inter , s_ab)
        else:
            ## THE ALGORITHM FOR DISCOVERING **ALL POSISIONS** OF TOH GAME IS :
            ## 1/ move all disks but the biggest form start to end
            ## 2/ then move biggest disk from start to inter
            ## 3/ then move all disks but the biggest form end to start
            ## 4/ then move biggest disk from inter to end
            ## 5/ then move all disks but the biggest form start to end
            ## in the same time, note all ABC notations and add edges to the graph
            self._discoverPositions(source, dest, inter, graphe, nb_disques-1)
            s_depart = self.getABC()
            source.moveTo(inter)
            s_inter = self.getABC()
            graphe.add_edge(s_depart , s_inter)
            
            self._discoverPositions(dest, source, inter, graphe, nb_disques-1)
            s_inter = self.getABC()
            inter.moveTo(dest)
            s_arrivee = self.getABC()
            graphe.add_edge(s_inter , s_arrivee)
            
            self._discoverPositions(source, dest, inter, graphe, nb_disques-1)
