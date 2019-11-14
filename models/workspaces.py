import datetime
import hashlib
import logging
import secrets
from operator import attrgetter

import bcrypt
from google.cloud import ndb
from models import get_db
from translations.loader import get_translation
from utils.check_environment import is_local
from utils.email_helper import send_email

client = get_db()


class Workspace(ndb.Model):
    title = ndb.StringProperty()
    slug = ndb.StringProperty()