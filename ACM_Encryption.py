"""
ACM_Encryption.py: File to encrypt or decrypt an RGB image using Arnold's Cat Map
"""
import numpy as np
from Statistical_Analysis import average_correlation

"""
Applies the confusion step to an RGB image using Arnold's Cat Map

Parameters: 

1. image: numpy n-dimensional array of the pixel values of the image
2. iterations : number of iterations to apply the matrix to the image
3. ACMMatrix: 2x2 numpy array used to scramble the image
4. compute_correlation: boolean value to determine if it is needed to compute the correlation at each iteration

Return Value:
1. tuple[np.ndarray, int, float]: returns a tuple containing the scrambled image, its average correlation, and the number of iterations performed

2. np.ndarray: returns the scrambled image

"""
def ACM_Encrypt(image: np.ndarray, 
                iterations: int, 
                ACMMatrix: list[list[int]], 
                compute_correlation: bool = False
               ) -> tuple[np.ndarray, float, int] | np.ndarray:
    
    min_iter: int = 0
    min_correlation: float = 1.0
 
    _, size, channels = np.array(image).shape
    current_image: np.ndarray = np.array(image).copy()
    x_image, y_image = np.meshgrid(np.arange(size), np.arange(size))

    nx_image, ny_image = np.dot(ACMMatrix, [x_image.flatten(), y_image.flatten()]) % size
    nx_image, ny_image = nx_image.reshape(x_image.shape), ny_image.reshape(y_image.shape)

    transformed_image: np.ndarray = np.zeros((size, size, channels)).astype(np.uint8)
    ny_image, y_image = size - ny_image - 1, size - y_image - 1
    
    for i in range(iterations):
        transformed_image[ny_image, nx_image] = current_image[y_image, x_image]
        current_image = transformed_image.copy()

        if compute_correlation:
            current_correlation: float = average_correlation(current_image)
            if current_correlation < min_correlation:
                min_correlation = current_correlation
                min_iter = i + 1

    image = current_image

    return (image, min_correlation, min_iter) if compute_correlation == True else image