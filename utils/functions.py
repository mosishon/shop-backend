import hashlib
from typing import BinaryIO


def generate_sha256_hash(file: BinaryIO):
    try:
        sha256_hash = hashlib.sha256()

        for chunk in file:
            sha256_hash.update(chunk)

        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None
    except Exception as e:
        raise e
