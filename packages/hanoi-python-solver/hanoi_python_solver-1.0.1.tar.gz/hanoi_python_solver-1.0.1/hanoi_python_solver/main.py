from typing import List, Tuple
from hanoi import Hanoi
from network import Network
from poteau import Poteau

    
def test() -> None:
    net = Network.fromAdjacencyMatrix("./src/adj.txt")
    if(net == None):
        print("pas de Network : arret du test")
    else:
        # net = Network()
        # retour = net.add_edge("A","B",85)
        # retour = net.add_edge("A","E",173)
        # retour = net.add_edge("B","F",80)
        # retour = net.add_edge("B","G",68)
        # retour = net.add_edge("A","C",217)
        # retour = net.add_edge("C","G",186)
        # retour = net.add_edge("C","H",103)
        # retour = net.add_edge("D","H",183)
        # retour = net.add_edge("E","J",314)
        # retour = net.add_edge("H","J",167)
        # retour = net.add_edge("F","I",250)
        # retour = net.add_edge("F","I",260)
        # retour = net.add_edge("I","J",84)

        dot = net.DOT_description()
        print(dot)
        print(f'edges = {net.edge_list_size()}')
        print(f'nodes = {net.nodes_list_size}')
        z = net.containsNode("E")
        print(f'net contains E = {z}')
        yy = net.dijkstra("A","J")
        print(yy)

        p1 = Poteau.createFromABC("AABCB",1)
        p2 = Poteau.createFromABC("AABCB",2)
        p3 = Poteau.createFromABC("AABCB",3)
        
        print(f"{p1}")
        print(f"{p2}")
        print(f"{p3}")
        
        reponse = "possible" if p3.checkMove(p1) else "impossible"
        print(f"mouvement de 3 vers 1 est {reponse}")

        print(f"{p1}")
        print(f"{p2}")
        print(f"{p3}")
        
        try:
            h = Hanoi(6)
        except Exception as e:
            print(f"impossible de créer Hanoi car {e.args}")
        else:
            useHanoi(h)
            
        print("FIN")
    
    
def useHanoi(h:Hanoi) -> None:
    moves:List[Tuple[int, int]] = [
        (1,2),
        (1,3),
        (2,3),
        (1,2)
    ]
    print(f"{h.getABC()}")
    for m in moves:
        print(f"move {m}")
        h.move(m)
        print(f"{h.getABC()}")
        
    possibles = h.possibleMoves()
    print(f"possibles {possibles}\n")
    
    resu = h.pathToSolution("C" * h.nbDisks)
    
    print(f"resu {resu}")
test()