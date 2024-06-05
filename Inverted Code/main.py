"""
main.py: The following 2 methods are the only difference between the original methodology 
and the inverted one in terms of functionality 
"""
def encrypt(size: str, image: np.ndarray) -> tuple[np.ndarray, int]:
    Phase1: np.ndarray = KTM_Encrypt(image, True)
    _, _, iters = ACM_Encrypt(Phase1, *ACM_Key[size], True)
    encrypted: np.ndarray = ACM_Encrypt(Phase1, iters, ACM_Key[size][1])
    return encrypted, iters

def decrypt(iters: int, size: str,  path: str, modified_key: bool = False) -> None:
    title: str = os.path.splitext(os.path.split(path)[1])[0]
    title = title.split('-')[0]
    name: str = "{name}-decrypted.png" if not modified_key else "{name}-decrypted-modified-key.png"

    with open(path) as im:
        image: np.ndarray = np.array(im)
        path = name.format(name = title)

        if modified_key:
            Phase1: np.ndarray = ACM_Encrypt(image, ACM_Key_Modified[size][0] - iters, ACM_Key_Modified[size][1])
            decrypted: np.ndarray = KTM_Encrypt(Phase1, False, new_board)
            cv2.imwrite(f'Results/{size}/Decrypted/' + path, cv2.cvtColor(decrypted, cv2.COLOR_RGB2BGR))

        else:
            Phase1 = ACM_Encrypt(image, ACM_Key[size][0] - iters, ACM_Key[size][1])
            decrypted = KTM_Encrypt(Phase1, False)
            cv2.imwrite(f'Results/{size}/Decrypted/' + path, cv2.cvtColor(decrypted, cv2.COLOR_RGB2BGR))

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

    with open('inverted_numerical_results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Size', 'Title', 'NPCR', 'UACI', 'Entropy', 'Correlation', "H", "V", "D"])
        writer.writerows(results)
