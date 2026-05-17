import hashlib


def generate_checksum(file_path: str) -> str:
    """
    Generates SHA256 checksum for a file.
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()