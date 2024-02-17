from .bdarg import Bdarg
from .bdsarg import Bdsarg
from .body import Body
from .bodies import Bodies
import math
import numpy as np

class RunBodies:
    def __init__(self,bn:int,arg:Bdsarg,tms=0.1):
        args=[]
        for v in arg:
            args.append((v[0]*math.sqrt(3),
                       np.array(v[1]),
                       np.array(v[2])))
        self.bds=Bodies(bn,arg,tms)
        
    def run(self,t:int)->None:
        self.bds.run(t)
    
    def getpos(self)->list:
        return self.bds.getpos()


  