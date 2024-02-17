import numpy as np

class Body:
    def __init__(self, weight, pos0, v0):
        '''
        weight:The weight of the body
        pos0:the position of the body,like[2,-4,0]
        v0:the velocity of the body,like[3,-1,7]
        '''
        self.m = weight
        self.pos = np.array(pos0)
        self.v = np.array(v0)

    def update(self, others, delta_t)->None:
        

        ft = np.array([0, 0, 0])
        for bodyi in others:
            
            ft_dir = (bodyi.pos - self.pos) / np.linalg.norm(bodyi.pos - self.pos)
            
            ft = ft + (bodyi.m * self.m / sum(np.square(bodyi.pos - self.pos))) * ft_dir
        at = ft / self.m
        
        self.pos = self.pos + self.v * delta_t + 0.5 * at * (delta_t ** 2)
        
        self.v = self.v + at * delta_t