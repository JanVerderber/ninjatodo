import logging

from google.cloud import ndb
from models import get_db


client = get_db()


class Workspace(ndb.Model):
    title = ndb.StringProperty()
    slug = ndb.StringProperty()

    # properties (ordered by alphabet)
    @property
    def get_id(self):
        return self.key.id()

    # class methods (ordered by alphabet)
    @classmethod
    def create(cls, title, slug):
        with client.context():
            # check if there's any workspaces with the same slug already
            workspace = cls.query(cls.slug == slug).get()

            if not workspace:  # if user does not yet exist, create one

                # create the workspace object and store it into Datastore
                workspace = cls(title=title, slug=slug)
                workspace.put()

                return True, workspace, "Success"  # succes, workspace, message
            else:
                return False, None, "Workspace with this slug is already created. Please try again with new slug."

    @classmethod
    def fetch(cls, title=True, slug=True, limit=None, cursor=None):
        with client.context():
            workspaces, next_cursor, more = cls.query(cls.title == title, cls.slug == slug).fetch_page(limit, start_cursor=cursor)

            # this fixes the pagination bug which returns more=True even if less users than limit or if next_cursor is
            # the same as the cursor
            logging.warning("More:")
            logging.warning(more)
            logging.warning(type(more))
            if limit and len(workspaces) < limit:
                return workspaces, None, False

            logging.warning("More 2:")
            logging.warning(more)
            logging.warning(type(more))

            try:
                return workspaces, next_cursor.urlsafe().decode(), more
            except AttributeError as e:  # if there's no next_cursor, an AttributeError will occur
                return workspaces, None, False
