import hashlib
import os

def calculate_file_hash(file_path, hash_algorithm="sha256"):
    """
    Calculates the hash of a file using MD5, SHA-1, or SHA-256.
    Reads file in binary chunks (64KB) to optimize memory for large files.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Map target string to hashlib function
    algo_name = hash_algorithm.lower().replace("-", "")
    if algo_name == "md5":
        hasher = hashlib.md5()
    elif algo_name == "sha1":
        hasher = hashlib.sha1()
    elif algo_name == "sha256":
        hasher = hashlib.sha256()
    else:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    chunk_size = 65536  # 64 KB chunks
    with open(file_path, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            hasher.update(data)

    return hasher.hexdigest()

def verify_file_integrity(file_path, expected_hash, hash_algorithm="sha256"):
    """
    Compares the calculated file hash against an expected hash (case-insensitive).
    """
    try:
        calculated = calculate_file_hash(file_path, hash_algorithm)
        return {
            "success": True,
            "calculated_hash": calculated,
            "match": calculated.lower() == expected_hash.strip().lower()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
