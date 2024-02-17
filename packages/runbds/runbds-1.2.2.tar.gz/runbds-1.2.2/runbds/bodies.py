from .body import Body
from .bdsarg import Bdsarg
import numpy as np

class Bodies:
    def __init__(self,bn:int,arg:Bdsarg,tms=0.1):
        self.stars=[Body(arg[i][0],arg[i][1],arg[i][2]) for i in range(0,bn)]
        self.TIMESTEP = tms
    
    def run(self,t:int)->None:
        if t<self.TIMESTEP:raise RuntimeError("time error!")
        for _ in np.arange(0,t/self.TIMESTEP):
            for body in self.stars:
                starscopy = self.stars[:]
                starscopy.remove(body)
                body.update(starscopy,self.TIMESTEP)
    
    def getpos(self)->list:
        poses=[]
        for star in self.stars:
            poses.append(star.pos)   
        return poses