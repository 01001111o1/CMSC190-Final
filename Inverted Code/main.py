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
