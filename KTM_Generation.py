"""
KTM_Generation.py: File to generate a Knight's Tour Matrix
"""
from heapq import heappush, heappop
import numpy as np

"""
Knight's x and y movement
"""
moves: list[list[int]] = [[1, -2], [2, -1], [2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2]]

"""
Returns 1 if a cell with coordinates x, y is within the bounds of the board with dimensions m x n and 0 otherwise
"""
def is_safe(x: int, y: int, board: np.ndarray) -> int:
    return 1 if (0 <= x < len(board) and 0 <= y < len(board[0]) and board[x][y] == 0) else 0

"""
Returns the number of possible cells a knight can go to given its current position x, y
"""	
def get_degree(x: int, y: int, board: np.ndarray) -> int:
    return np.sum([is_safe(*np.add([x, y], moves[i]), board) for i in range(8)])

"""
Generates a Knights Tour Matrix on a board of dimensions m x n filled with 0s with a starting index of x, y
"""
def generateKTM(x: int, y: int, board: np.ndarray) -> np.ndarray:
    
    p: int = 1
    board[x, y] = p
    
    for _ in range(len(board) * len(board[0])):
        pq: list[tuple] = []

        for i in range(8):
            nx, ny = np.add([x, y], moves[i])
            
            if is_safe(nx, ny, board):
                degree: int = get_degree(nx, ny, board)
                heappush(pq, (degree, i))
        
        if len(pq) > 0:
            _, i = heappop(pq)
            x, y = np.add([x, y], moves[i])
            p += 1
            board[x, y] = p

    return board