
from typing import List, Self
from abc_notation import ABC_Notation

class Poteau:
    """
    Defines a rod (poteau in french) on which disks can be slid.
    """
    
    def __init__(self, disks:List[int], id:int) -> None:
        """creates a new Poteau with a list of disks and an Id. 
        The list of disks can be empty.

        Args:
            disks (List[int]): the list of disks ordered by the size of the disks (1st the biggest - last the smallest)
            id (int): a unique Id for this Poteau (generally 1, 2 or 3 ... this package doesn't accept more Poteau)
        """
        self._disks:List[int] = []
        self._id = id
        counter = 0
        for disk in disks:
            if counter == 0:
                self._disks.append(disk)
            else:
                # check if all is OK
                if self._disks[counter - 1] < disk:
                    raise ValueError(f"On ne peut pas empiler un gros disque sur un petit ({disk})")
                else:
                    self._disks.append(disk)
            counter +=1

    @classmethod
    def createFromABC(cls, abc_notation:str, id:int):
        disks = ABC_Notation.generateDisks(abc_notation, id)
        ret = Poteau(disks, id)
        return ret
    
    @property
    def isEmpty(self):
        return len(self._disks) == 0
    
    @property
    def size(self) -> int:
        return len(self._disks)
    
    @property
    def sizeOfLastDisk(self) -> int | None:
        if self.isEmpty:
            return None
        return self._disks[self.size - 1]
    
    def popLastDisk(self) -> int | None:
        """
        Pops out the smallest disk from this Poteau.

        Returns:
            int | None: the size of the removed disk or None if Poteau was empty
        """
        if self.isEmpty:
            return None
        last_index = self.size - 1
        # get the value we poped out from the _disks array
        ret = self._disks[last_index]
        # slice the _disks array
        self._disks = self._disks[0:last_index]
        return ret
    
    def getDisks(self) -> List[int]:
        return self._disks
    
    def pushDisk(self, size_of_disk:int) -> bool:
        """
        the given disk will be slid on this rod if the size of the current
        last disk is bigger than the given size

        Args:
            size_of_disk (int): the size of the disk to be add to this Poteau

        Returns:
            bool: True if the disk was added or False otherwise.
        """
        last_disk = self.sizeOfLastDisk
        if last_disk == None or last_disk > size_of_disk:
            self._disks.append(size_of_disk)
            return True
        return False
    
    def moveTo(self, poteau:Self) -> bool:
        """
        moves the last disk to an other Poteau.

        Args:
            poteau (Poteau): an other Poteau

        Returns:
            bool: True if move succeeded, False otherwise
        """
        last_disk = self.popLastDisk()
        if last_disk == None:
            return False
        else:
            # try to push our last disk on the given Poteau
            resu = poteau.pushDisk(last_disk)
            if not resu:
                # push failed on poteau
                # so reinsert our last disk previously popped out
                self.pushDisk(last_disk)
            return resu
        
        
    def checkMove(self, poteau_destination:Self) -> bool:
        """
        Checks if a move from me to poteau_destination is possible

        Args:
            poteau_destination (Self): a poteau

        Returns:
            bool: True if the move is possible - False otherwise
        """
        my_last_disk = self.sizeOfLastDisk
        if my_last_disk == None:
            return False
        dest_last_disk = poteau_destination.sizeOfLastDisk
        if dest_last_disk == None:
            return True
        else:
            return my_last_disk < dest_last_disk
    
    def __str__(self) -> str:
        return f"P{self._id} {self._disks}"
    
    
    