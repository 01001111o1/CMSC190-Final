ENHANCED RGB IMAGE ENCRYPTION: INTEGRATING ARNOLDS CAT MAP AND KNIGHTS TOUR WITH 8-NEIGHBORHOOD ADDITION FOR SECURE IMAGE TRANSMISSION

Authors: Jehanne Eliza F. Criseno
         Sean Thomas C. Vizconde

Adviser: Lee J. Javellana

================================================================================================================================

A special problem submitted to the Department of Mathematics and Computer Science's  College of Science in The University of the Philippines Baguio, Baguio City

================================================================================================================================

The project consists of the following source files:
	1. main.py: Main file to run to generate image and numerical results
	2. ACM_Encryption.py: File to encrypt or decrypt an RGB image using Arnold's Cat Map
	3. ACM_Generation.py: File to generate a 2x2 Arnold's Cat Map for a given image size N
	4. KTM_Encryption.py: File to encrypt or decrypt an RGB image using Knight's Tour Matrix
	5. KTM_Generation.py: File to generate a Knight's Tour Matrix
	6. Statistical_Analysis.py: File containing the functions to generate the numerical results for the project
	7. keys.py: File containing the ACM Matrices, number of iterations for minimum correlation, and the modified keys used in the datasets for the original encryption scheme

Under the subfolder named "Inverted Code" there are the following source files:

	1. main.py: contains three methods, encrypt, decrypt, and generate_Numerical_Results which are the only methods different from the file with the same name in the main directory
	3. keys.py: File containing the ACM Matrices, number of iterations for minimum correlation, and the modified keys used in the datasets for the inverted encryption scheme

In main.py, run the following snippet to generate the results

if __name__ == "__main__":
    generate_DAA_Dataset()
    generate_Numerical_Results()
    decrypt_all()
    decrypt_all(True)

The first method generates a pair of cipher images with which the first one is the encrypted dataset image and the second one is another encrypted image but with the plaintext image being modified by a single pixel

The second method generates all numerical results

The third method decrypts the encrypted images using the original keys

The fourth method decrypts the encrypted images using the modified keys which is then the required result for key sensitivity

Numerical results will be stored in a CSV file named "original_numerical_results.csv" and replacing the aforementioned functions in main.py will generate the required results for the inverted code and store it in a csv file named "inverted_numerical_results.csv"

Non-numerical results are stored in the "Results" folder which is then further sub-divided by image size (i.e., 350, 500, etc.)

Within each sub-folder, the following folders can be found

	1. Decrypted: Set of pictures decrypted using the original key
	2. Differential_Attack: Contains a folder for each picture in the dataset (i.e., a new folder for "airplane.png", "baboon.png", etc.) where each folder contains a pair of pictures {name}-original.png and {name}-modified.png denoting the encrypted images from the original and modified dataset images, respectively
	3. ModifiedKey: Set of pictures decrypted using the modified key


================================================================================================================================
Further clarifications and concerns may be directed to the following contacts

1. jfcriseno@up.edu.ph
2. scvizconde@up.edu.ph

================================================================================================================================
