
from typing import Dict, List, Tuple


class ABC_Notation:
    """
    ABC notation for a Tower of Hanoi game. A is for 1st rod, B for the second
    and C for the third. In this package, only three rods are valid.
    The length of an ABC notation gives the number of disks in the game. A classic 
    TOH game with 5 disks begins at position AAAAA and the goal is to reach CCCCC.
    """
    
    @classmethod
    def checkNotationABC(cls, notation:str) -> bool:
        notation_upper = notation.upper()
        if notation != notation_upper:
            #raise ValueError(f"La notation \"{notation}\" doit être en majuscule.")
            return False
        
        for c in notation:
            if c == 'A' or c == 'B' or c == 'C':
                continue
            #raise ValueError(f"La notation \"{notation}\" ne doit comporter que les lettres A, B et C.")
            return False
        
        return True
    
    @classmethod
    def generateDisks(cls, notation:str, id:int) -> List[int]:
        """Generates a list of disks sizes. Example : "AAA" for id = 1
        returns [3,2,1]. But "AAA" for id = 2, generates []. "ABC" for id = 1 
        returns [3], for id = 2 returns [2] and for id=3 returns [1]
        

        Args:
            notation (str): the ABC notation
            id (int): the id of the rod (Poteau) to take in account

        Raises:
            ValueError: if notation isn't well formed
            ValueError: if id is different from 1, 2 or 3

        Returns:
            List[int]: a list of disks sizes
        """
        if not cls.checkNotationABC(notation):
            raise ValueError(f"La notation \"{notation}\" n'est pas correctement formée.")
        ret:List[int] = []
        combien = len(notation)
        lettre:str = ""
        if id == 1:
            lettre = "A"
        elif id == 2:
            lettre = "B"
        elif id == 3:
            lettre = "C"
        else:
            raise ValueError(f"L'id du poteau doit être 1, 2 ou 3 (au lieu de {id})")
        for c in notation:
            if c==lettre:
                ret.append(combien)
            combien -= 1
            if combien == 0:
                break
        return ret
                
            
    @classmethod
    def movementBetween(cls, notation1:str, notation2:str) -> Tuple[int,int] | None:
        """
        Detects the move done between the two ABC notation strings provided. This 
        method doesn't verify if the move is legal (perhaps you may have put a 
        disk on a smaller one)

        Args:
            notation1 (str): an ABC notation string
            notation2 (str): an other ABC notation string

        
        Returns:
            Tuple[int,int] | None: the move done or None if string weren't correct 
            ABC notations or if there was more than 1 difference between the two 
            strings or if there is no difference between the two strings.
        """
        if not ABC_Notation.checkNotationABC(notation1) or not ABC_Notation.checkNotationABC(notation2):
            return None
        l1 = len(notation1)
        l2 = len(notation2)
        if l1 != l2:
            return None
        nb_differences:int = 0
        diff:Dict[str, str]={}
        position:int = -1
        for x in range(l1):
            c1 = notation1[x]
            c2 = notation2[x]
            if c1 != c2:
                nb_differences += 1
                position = x
                diff = {
                     "car1": c1,
                     "car2": c2
                }
            if nb_differences == 2:
                return None

        if nb_differences == 0:
            return None
        
        # there's only one diff here, at position position
        
        retour:Tuple[int, int] = (0,0)
        c1 = diff.get("car1")
        c2 = diff.get("car2")
        try:
            legal_move = notation2[position + 1:].index(str(c2)) < 0
        except ValueError:
            legal_move = True
        if c1 == "A" and c2 == "B":
            retour = (1,2)
        elif c1 == "B" and c2 == "C":
            retour = (2,3)
        elif c1 == "A" and c2 == "C":
            retour = (1,3)
        elif c1 == "B" and c2 == "A":
            retour = (2,1)
        elif c1 == "C" and c2 == "B":
            retour = (3,2)
        elif c1 == "C" and c2 == "A":
            retour = (3,1)
        else:
            return None
        if not legal_move:
            return None
        return retour