from flask_cors import CORS

from app.config import DATASTORE_ACCESS_KEY, DATASTORE_SECRET_KEY
from app.datastore import BaseDatastore, MinioDatastore

cors = CORS()

datastore: BaseDatastore = MinioDatastore(DATASTORE_ACCESS_KEY, DATASTORE_SECRET_KEY)
