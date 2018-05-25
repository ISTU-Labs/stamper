import bcrypt
import mmh3 as mmh3


def get_hashed_password(plain_text_password):
    # Хэширует пароль в фазе его задания
    # Используется модуль bcrypt, соль записывается в сам хэш
    plain_text_password = as_bytes(plain_text_password)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt()).decode("utf-8")


def check_password(plain_text_password, hashed_password):
    # Проверка пароля. В модуле bcrypt соль записана в самом хеше
    plain_text_password = as_bytes(plain_text_password)
    print(type(plain_text_password), type(hashed_password))
    return bcrypt.checkpw(plain_text_password, hashed_password.encode("utf-8"))


def as_bytes(s):
    if type(s) == str:
        return s.encode('utf-8')
    return s


def hexdigest(digest):
    """Convert byte digest to
    hex digest
    Arguments:
    - `digest`: Byte array representing
    digest
    """
    if type(digest) in (tuple, list):
        digest = joindigest(digest)
    if type(digest) == str:
        return digest		# implied, that string is a digest already
    if type(digest) == int:
        digest = bindigest(digest)
    return ''.join(["{:02x}".format(b) for b in digest])


def bindigest(digest, bs=16):
    if type(digest) in (tuple, list):
        digest = joindigest(digest)
    if type(digest) == str:
        return bytearray.fromhex(digest)
    if type(digest) == int:
        digest = digest.to_bytes(bs, byteorder='little')
    return digest


def intdigest(digest):
    if type(digest) in (tuple, list):
        digest = joindigest(digest)
    if type(digest) == int:
        return digest
    if type(digest) == str:
        digest = bytearray.fromhex(digest)
    return int.from_bytes(digest, byteorder='little')


def hash128(content):
    return mmh3.hash_bytes(content)


def hash128_int(content):
    return intdigest(hash128(content))


def splitdigest(digest):
    """Splits 128bit hash into two
    64bit numbers."""
    d = bindigest(digest)
    l, h = intdigest(d[:8]), intdigest(d[8:])
    return l, h


two64 = 1 << 64


def joindigest(digest):
    l, h = digest
    if l < 0:
        l = two64 - l
    if h < 0:
        h = two64 - h
    l = bindigest(l, bs=8)
    h = bindigest(h, bs=8)
    return l + h
