"""
KTM_Encryption.py: File to encrypt or decrypt an RGB image using Knight's Tour Matrix
"""
import numpy as np
import cv2
from copy import deepcopy
from KTM_Generation import generateKTM
from numba import jit 

#Generates a 9x8 KTM matrix with starting coodrdinates at 5,7
board = np.zeros((9, 8))
b_rows, b_cols = board.shape
board = generateKTM(5, 7, board)

"""
Returns the pixel value at coordinates row, col if it is within the image bounds and 0 otherwise
"""
@jit(nopython = True)
def isValid(image: np.ndarray, row: int, col: int) -> int:
    height, width = image.shape
    return 0 if (row < 0 or row >= height or col < 0 or col >= width) else image[row, col]

"""
Performs 8N addition on a pixel at coordinates row, col if decrypt is set to false and 8N subraction otherwise
"""
@jit(nopython = True)
def _8NAddition(image: np.ndarray, row: int, col: int, decrypt: bool = False) -> int:
    res: int = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if(i == 0 and j == 0): 
                continue
            res += isValid(image, row + i, col + j)
    
    new_pixel: int = image[row, col] + res if decrypt == False else image[row, col] - res

    return new_pixel % 256

"""
Encrypts a single channel of an RGB image using Knight's Tour and 8 Neighborhood addition
"""
def encrypt_channel(image: np.ndarray) -> np.ndarray:

    current_image: np.ndarray = np.array(deepcopy(image))
    height, width = image.shape    
    sequence_map: np.ndarray = np.zeros((height, width))
    tile: np.ndarray = np.tile(board, (height // b_rows, width // b_cols))
    sequence_map[:len(tile), :len(tile[0])] = tile

    for i in range(height):
        for j in range(width):
            current_image[i, j] = _8NAddition(current_image, i, j)

    for j in range(1, b_rows * b_cols + 1):
        for i, j in np.argwhere(sequence_map == j):
            current_image[i, j] = _8NAddition(current_image, i, j)

    for i, j in np.argwhere(sequence_map == 0):
        current_image[i, j] = _8NAddition(current_image, i, j)

    return current_image

"""
decrypts a single channel of an RGB image using Knight's Tour and 8 Neighborhood subtraction
"""
def decrypt_channel(image : np.ndarray, board = board) -> np.ndarray:

    current_image: np.ndarray = np.array(deepcopy(image))
    current_image = cv2.flip(current_image, -1)
    height, width = image.shape    
    sequence_map: np.ndarray = np.zeros((height, width))
    tile: np.ndarray = np.tile(board, (height // b_rows, width // b_cols))
    sequence_map[:len(tile), :len(tile[0])] = tile
    sequence_map = cv2.flip(sequence_map, -1)

    for i, j in np.argwhere(sequence_map == 0):
        current_image[i, j] = _8NAddition(current_image, i, j, True)

    for j in range(b_rows * b_cols, 0, -1):
        for i, j in np.argwhere(sequence_map == j):
            current_image[i, j] = _8NAddition(current_image, i, j, True)

    for i in range(height):
        for j in range(width):
            current_image[i, j] = _8NAddition(current_image, i, j, True)

    current_image = cv2.flip(current_image, -1)
    return current_image

"""
Encrypts or decrypts an RGB image using Knight's Tour Matrix and 8 Neighborhood addition / subtraction
"""
def KTM_Encrypt(image: np.ndarray, encrypt: bool = True, board: np.ndarray = board) -> np.ndarray:

    current_image: np.ndarray = deepcopy(image)

    R, G, B = image[:, :, 0], image[:, :, 1], image[:, :, 2]

    if encrypt == True:
        Red: np.ndarray = encrypt_channel(R)
        Green: np.ndarray = encrypt_channel(G)
        Blue: np.ndarray = encrypt_channel(B)
    else:
        Red = decrypt_channel(R, board)
        Green = decrypt_channel(G, board)
        Blue = decrypt_channel(B, board)            

    current_image = cv2.merge((Red, Green, Blue))

    return current_image

