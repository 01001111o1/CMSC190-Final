"""
main.py: Main file to run to generate image and numerical results
"""
import csv
import os 
import numpy as np
import cv2
from KTM_Encryption import KTM_Encrypt
from ACM_Encryption import ACM_Encrypt
from Statistical_Analysis import correlation, split_correlation, compute_entropy, compute_NPCR, compute_UACI
from keys import ACM_Key, ACM_Key_Modified, iters, new_board
from PIL.Image import open as PIL_open
import copy

"""
Retrieves all dataset sizes
"""
sizes: list[str] = os.listdir("Dataset/")

"""
Creates a directory in the specified path parameter if it does not exist and does nothing otherwise
"""
def cd(path: str) -> None:
	if os.path.exists(path) and os.path.isdir(path):
		pass
	else:
		os.makedirs(path)

"""
Creates encrypted images using the image specified by the path parameter and its slightly modified version
"""
def create_single_DAA(size: str, path: str) -> None: 
    title: str = os.path.splitext(os.path.split(path)[1])[0]
    res_path: str = f'Results/{size}/Differential_Attack/{title}'
    cd(res_path)
    name: str = "{name}-{type}.png"

    original: np.ndarray = np.array(PIL_open(path))
    modified: np.ndarray = copy.deepcopy(original)
    modified[4, 6] = 255 - modified[4, 6]
    _original_encrypted, _ = encrypt(size, original)
    _modified_encrypted, _ = encrypt(size, modified)

    path1: str = name.format(name = title, type = 'original')
    path2: str = name.format(name = title, type = 'modified')

    cv2.imwrite(res_path + "/" + path1, cv2.cvtColor(_original_encrypted, cv2.COLOR_RGB2BGR))
    cv2.imwrite(res_path + "/" + path2, cv2.cvtColor(_modified_encrypted, cv2.COLOR_RGB2BGR))

"""
Creates the differential attack analysis dataset for all images in all sizes
"""
def generate_DAA_Dataset() -> None:
    for size in sizes:
        path: str = f'Dataset/{size}/'
        images: list[str] = os.listdir(path)

        for image in images:
            image_path: str = path + image
            create_single_DAA(size, image_path)		

"""
Generates the numerical results for every image in all sizes
"""
def generate_Numerical_Results() -> None:
    results = []
    for size in sizes:
        path: str = f'Results/{size}/Differential_Attack/'
        titles: list[str] = os.listdir(path)

        for title in titles:
            image_path: str = path + title + "/"
            images: list[str] = os.listdir(image_path)
            modified: str = image_path + images[0]
            original: str = image_path + images[1]
            _entropy: float = compute_entropy(original)
            _correlation: float = correlation(original)
            h, v, d = split_correlation(original) 
            NPCR: float = compute_NPCR(modified, original)
            UACI: float = compute_UACI(modified, original)
            results.append([size, title, NPCR, UACI, _entropy, _correlation, h, v, d])

    with open('original_numerical_results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Size', 'Title', 'NPCR', 'UACI', 'Entropy', 'Correlation', "H", "V", "D"])
        writer.writerows(results)


"""
Decrypts an RGB image using Knight's Tour Matrix and Arnold's Cat Map

Parameters:
1. iters: number of iterations to apply the ACM matrix on the image
2. size: Size of the image
3. path: path containing the image to decrypt
4. modified_key: decrypts the image using the same keys used to encrypt if it is set to false and a modified key otherwise
"""
def decrypt(iters: int, size: str,  path: str, modified_key: bool = False) -> None:
    title: str = os.path.splitext(os.path.split(path)[1])[0]
    title = title.split('-')[0]
    name: str = "{name}-decrypted.png" if not modified_key else "{name}-decrypted-modified-key.png"

    with PIL_open(path) as im:
        image: np.ndarray = np.array(im)
        path = name.format(name = title)
        
        if modified_key:
            Phase1: np.ndarray = KTM_Encrypt(image, False, new_board)
            decrypted: np.ndarray = ACM_Encrypt(Phase1, ACM_Key_Modified[size][0] - iters, ACM_Key_Modified[size][1])
            cv2.imwrite(f'Results/{size}/ModifiedKey/' + path, cv2.cvtColor(decrypted, cv2.COLOR_RGB2BGR))
        else:
            Phase1 = KTM_Encrypt(image, False)
            decrypted = ACM_Encrypt(Phase1, ACM_Key[size][0] - iters, ACM_Key[size][1])
            cv2.imwrite(f'Results/{size}/Decrypted/' + path, cv2.cvtColor(decrypted, cv2.COLOR_RGB2BGR))

"""
Encrypts an RGB image using Knight's Tour Matrix and Arnold's Cat Map

Parameters:
1. size: size of the image
2. image: the image to be encrypted converted into an n-dimensional numpy array

Returns:
1. the encrypted image
2. number of iterations the ACM matrix was applied to the plaintext image
"""
def encrypt(size: str, image: np.ndarray) -> tuple[np.ndarray, int]:

    _, _, iters = ACM_Encrypt(image, *ACM_Key[size], True)
    Phase1: np.ndarray = ACM_Encrypt(image, iters, ACM_Key[size][1])
    encrypted: np.ndarray = KTM_Encrypt(Phase1, True)
    return encrypted, iters

"""
Decrypts every encrypted image in the dataset using the original 
keys if modified_key is set to false and uses the modified keys otherwise
"""
def decrypt_all(modified_key: bool = False) -> None:
	for size in sizes:
		path: str = f'Results/{size}/'
		images: list[str] = [file for file in os.listdir(path) if file.endswith(".png")]

		for index, image in enumerate(images):
			image_path: str = path + image
			decrypt(iters[size][index], size, image_path, modified_key)

if __name__ == "__main__":
    #generate_DAA_Dataset()
    generate_Numerical_Results()
    #decrypt_all()
    #decrypt_all(True)
    