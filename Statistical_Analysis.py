"""
Statistical_Analysis.py: File containing the functions to generate the numerical results for the project
"""
import numpy as np
from numpy.random import choice
from PIL.Image import open
import matplotlib.pyplot as plt
from skimage.measure import shannon_entropy

"""
Array containing the slice indices for the horizontal, vertical, and diagonal orientations
"""
indices = [ 
            [slice(None, None), slice(None, -1), slice(None, None), slice(1, None)], 
            [slice(None, -1), slice(None, None), slice(1, None), slice(None, None)], 
            [slice(None, -1), slice(None, -1), slice(1, None), slice(1, None)]       
          ]

"""
Calculates the pixel wise correlation in a single orientation
"""
def calculate_correlation(image: np.ndarray, idx: list[slice]) -> float:
    x: np.ndarray = image[idx[0], idx[1]].flatten()
    y: np.ndarray = image[idx[2], idx[3]].flatten()
    return np.corrcoef(x, y)[0, 1]

"""
Calculates the averaged pixel wise correlation in all three orientations given a n-dimensional numpy array
"""
def average_correlation(image: np.ndarray) -> float:
    return np.mean([calculate_correlation(image, indices[i]) for i in range(3)])

"""
Calculates the averaged pixel wise correlation in all three orientations given a path to an image
"""
def correlation(path: str) -> float:
    with open(path) as im:
        image: np.ndarray = np.array(im)
        return average_correlation(image)

"""
Returns a list containing the pixel wise correlations in the horizontal, vertical, and diagonal orientations
"""
def split_correlation(path: str) -> list[float]:
    with open(path) as im:
        image: np.ndarray = np.array(im)
        return [calculate_correlation(image, indices[i]) for i in range(3)]

"""
Creates a scatterplot containing the pixel wise correlations in the horizontal, vertical, and diagonal orientations
"""
def graph_correlation(path: str, num_samples: int = 5000, idx: list[list[slice]] = indices) -> None:

    image: np.ndarray = np.array(open(path))
    values: list[list[np.ndarray]] = []
    labels: list[str] = ["Horizontal", "Vertical", "Diagonal"]
    plt.figure(figsize=(15, 5))

    for i in range(3):
        x: np.ndarray = image[idx[i][0], idx[i][1]].flatten()
        y: np.ndarray = image[idx[i][2], idx[i][3]].flatten()
        rand_index: np.ndarray = choice(len(x), num_samples, replace=False)
        x_sampled: np.ndarray = x[rand_index]
        y_sampled: np.ndarray = y[rand_index]
        values.append([x_sampled, y_sampled])

    for i in range(3):
        plt.subplot(1, 3, i + 1)
        plt.title(f'{labels[i]} Correlation')
        plt.scatter(*values[i])

    plt.show()

"""
Splits an RGB image and returns the R, G, and B channels
"""
def split_RGB(path: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
	with open(path) as im:
		image: np.ndarray = np.array(im)
		return image[:, :, 0], image[:, :, 1], image[:, :, 2]

"""
Computes the shannon entropy of a given RGB image using the formula

H(m) = sum(p(m_i) log2(1/p_mi)) where i = 0, 1, ..., 255 
"""
def compute_entropy(path: str) -> float: 

	channels: tuple[np.ndarray, np.ndarray, np.ndarray] = split_RGB(path)
	return np.mean([shannon_entropy(channels[0]),
					shannon_entropy(channels[1]),
					shannon_entropy(channels[2])])

"""
Computes the Number of Pixel Change Rate (NPCR) of a given RGB image using the formula

sum(D_(i, j)) / (WxH) * 100% where 

D_(i, j) = 0 if image1[i, j] != image2[i, j] and 1 otherwise

for 0 <= i <= W - 1 and 0 <= j <= H - 1
where W, H represents the dimensions of the image
"""
def compute_NPCR(path1: str, path2: str) -> float:
	image1: np.ndarray = np.array(open(path1)).astype(float)
	image2: np.ndarray = np.array(open(path2)).astype(float)
	difference: int = np.count_nonzero(image1 - image2)
	NPCR: float = (difference / (np.prod(image1.shape))) * 100
	return NPCR

"""
Computes the Unified Averaged Changed Intensity (UACI) of a given RGB image using the formula

sum(|image1[i, j] - image2[i, j]| / 255.0) / (WxH) * 100%  
for 0 <= i <= W - 1 and 0 <= j <= H - 1
where W, H represents the dimensions of the image
"""
def compute_UACI(path1: str, path2: str) -> float:
    array1: np.ndarray  = np.array(open(path1)).astype(float)
    array2: np.ndarray  = np.array(open(path2)).astype(float)
    differences: np.ndarray = np.abs(array1 - array2) / 255.0
    UACI: float = np.mean(differences) * 100
    return UACI

