
from typing import List


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
                
            
        