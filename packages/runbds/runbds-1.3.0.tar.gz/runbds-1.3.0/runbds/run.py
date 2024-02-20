from . import RunBodies

GOOD_ARG=[
    [   
        1000,
        [3,5,7],
        [-3,5,-7]
    ],
    [
        1500,
        [-2,-4,-6],
        [-1,-2,-3]
    ],
    [   1700,
        [-7,-1,0],
        [2,-3,1]
    ]
]

def run_good_arg(t:int,arg:list=GOOD_ARG)->list:
    bds=RunBodies(3,arg)
    bds.run(t)
    return bds
   
    