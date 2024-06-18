import unicodedata


def bytes_to_mb(byte_size):
    mb_size = byte_size / (1024 * 1024)  # 1 MB = 1024 * 1024 bytes
    return mb_size


def normailize_file_name(file_name):
    return unicodedata.normalize('NFC', file_name)
