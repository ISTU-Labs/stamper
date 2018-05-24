import kyotocabinet as kc
from .hashes import hexdigest, hash128


class ImageStore:
    def __init__(self, dbname):
        self.dbname = dbname+".kch"  # Hash table
        self.db = None

        self._open()

    def _open(self):
        if self.db is None:
            self.db = kc.DB()
            if not self.db.open(self.dbname, kc.DB.OWRITER | kc.DB.OCREATE):
                raise IOError("open error: " +
                              str(db.error()), file=sys.stderr)
        assert self.db is not None

    def _close(self):
        if self.db is not None:
            self.db.close()
            self.db = None

    def save(self, content):
        if self.db is None:
            raise IOError("the database is not open")
        id = self._hash(content)
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


def get_img_store(imgstore, request):
    return imgstore


def includeme(config):
    """
    Инициализация хранилища изображений

    Для активации данной настройки добавить ``config.include('stamper.imgstore')``.

    """
    settings = config.get_settings()

    # use pyramid_tm to hook the transaction lifecycle to the request
    # config.include('pyramid_tm')

    # use pyramid_retry to retry a request when transient exceptions occur
    # config.include('pyramid_retry')

    imgstoreobj = ImageStore(settings["imgstore.dbname"])

    config.registry['imgstore'] = imgstoreobj

    # make request.dbsession available for use in Pyramid
    config.add_request_method(
        lambda request: get_img_store(imgstoreobj, request),
        'imgstore',
        reify=True
    )
