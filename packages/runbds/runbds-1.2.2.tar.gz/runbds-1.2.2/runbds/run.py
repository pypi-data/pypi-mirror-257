from .bdsarg import Bdsarg
from .bdarg import Bdarg
from . import RunBodies

GOOD_ARG=Bdsarg([
    Bdarg([1000,
           [3,5,7],
           [-3,5,-7]
           ]),
    Bdarg([1500,
          [-2,-4,-6],
          [-1,-2,-3]
          ]),
    Bdarg([1700,
          [-7,-1,0],
          [2,-3,1]
          ])
    ])

def run_good_arg(t:int,arg=GOOD_ARG)->list:
    bds=RunBodies(3,arg)
    bds.run(t)
    return bds
   
    