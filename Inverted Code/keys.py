"""
keys.py: File containing the ACM Matrices, number of iterations for minimum correlation, 
and the modified keys used in the datasets for the inverted encryption scheme
"""
import numpy as np

ACM_Key = {'317' : (4187, [[8, 195], [215, 185]]),
           '350' : (1200, [[313, 36], [94, 95]]),
           '316' : (1040, [[233, 129], [262, 255]]),
           '318' : (936, [[205, 203], [52, 277]]),
           '331' : (2490, [[7, 102], [232, 236]]),
           '500' : (600, [[493, 118], [349, 83]])}

ACM_Key_Modified = {'317' : (4187, [[9, 196], [215, 185]]),
                    '350' : (1200, [[314, 36], [94, 95]]),
                    '316' : (1040, [[234, 129], [262, 255]]),
                    '318' : (936, [[206, 203], [52, 277]]),
                    '331' : (2490, [[8, 102], [232, 236]]),
                    '500' : (600, [[494, 118], [349, 83]])}

iters = {'317' : [1508, 2316, 2800, 1626, 3750, 843, 1025, 344, 2755, 86],
		 '350' : [1003, 681, 204, 39, 917],
         '316' : [115, 718, 369, 720, 34], 
         '318' : [102, 109, 16, 76, 156],
         '331' : [1736, 394, 966, 650, 44],
         '500' : [479, 439, 350, 18, 442]} 

new_board = np.array([[53,  48,  43,  12,  71,  66,  41,  14],
                    [44,  11,  54,  47,  42, 13,  64, 67],
                    [49,  52,  45,  72,  65,  70,  15,  40],
                    [10,  55,  50,  57,  46,  61,  68,  63],
                    [51,  34,  37,  60,  69,  58,  39,  16],
                    [36,  9,  56,  27,  38,  23,  1,   62],
                    [33,  6,   35,  22,  59,  28,  17,  24],
                    [8,   21,  4,   31,  26,  19,  2,   29],
                    [5,   32,  7,   20,  3,   30,  25,  18]])