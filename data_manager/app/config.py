import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, "../../.env"))
load_dotenv(os.path.join(basedir, "../.env"))

TESTING = os.environ.get("TESTING") or False
DEVELOPMENT = os.environ.get("DEVEL") or False
DEV = DEVELOPMENT

DATASTORE_URI = os.environ.get("DATASTORE_URI") or "localhost:9000"
DATASTORE_ACCESS_KEY = os.environ.get("DATASTORE_ACCESS_KEY") or ""
DATASTORE_SECRET_KEY = os.environ.get("DATASTORE_SECRET_KEY") or ""
