from .bdarg import Bdarg

class Bdsarg:
    def __init__(self,arg:list[Bdarg]):
        self.arg=arg
    
    def __getitem__(self,i:int):
        return self.arg[i]
    
    def __setitem__(self, i:int, v):
        self.data[i] = v
        
    def __len__(self):
        return len(self.arg)