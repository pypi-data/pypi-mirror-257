from typing import List

class ABC_Notation:
    @classmethod
    def checkNotationABC(cls, notation: str) -> bool: ...
    @classmethod
    def generateDisks(cls, notation: str, id: int) -> List[int]: ...
