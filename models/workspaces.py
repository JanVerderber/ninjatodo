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

    # class methods (ordered by alphabet)
    @classmethod
    def create(cls, title, slug):
        with client.context():
            # check if there's any workspaces with the same slug already
            workspace = cls.query(cls.slug == slug).get()

            if not workspace:  # if user does not yet exist, create one
                hashed = None

                # create the workspace object and store it into Datastore
                workspace = cls(title=title, slug=slug)
                workspace.put()

                return True, workspace, "Success"  # succes, workspace, message
            else:
                return False, workspace, "Workspace with this slug is already created. Please try again with new slug."