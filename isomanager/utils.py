import hashlib


def hash(path):
    # Specify how many bytes of the file you want to open at a time
    BLOCKSIZE = 65536

    sha = hashlib.sha256()
    with open(path, 'rb') as kali_file:
        file_buffer = kali_file.read(BLOCKSIZE)
        while len(file_buffer) > 0:
            sha.update(file_buffer)
            file_buffer = kali_file.read(BLOCKSIZE)
    return sha.hexdigest()
