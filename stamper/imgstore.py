import kyotocabinet as kc
import mmh3 as mmh3


class ImageStore:
    def __init__(self, db_name):
        self.db_name = db_name+".kch"  # Hash table
        self.db = None

        self._open()

    def _open(self):
        if self.db is not None:
            self.db = kc.DB()
            if not db.open(self.db_name, DB.OWRITER | DB.OCREATE):
                raise IOError("open error: " +
                              str(db.error()), file=sys.stderr)

    def _close(self):
        if self.db is not None:
            self.db.close()
            self.db = None

    def save(self, content):
        if self.db is None:
            raise IOError("the database is not open")
        id = _hash(content)
        if not self.db.set(id, content):
            raise IOError("set error: " + str(db.error()), file=sys.stderr)
        return id

    def load(self, id):
        content = db.get(id)
        if content:
            return content

        raise IOError("get error: " + str(db.error()), file=sys.stderr)

    def start(self):
        self.db.begin_transaction()

    def commit(self, commit=True):
        self.db.end_transaction(commit)

    def _hash(self, content):
        int_d = hash128(content)
        return hexdigest(int_d)

    def __del__(self):
        self._close()


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
