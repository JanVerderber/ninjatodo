import logging

from google.cloud import ndb
from models import get_db
from models.user import User


client = get_db()


class WorkspaceUser(ndb.Model):
    id_workspace = ndb.IntegerProperty()
    id_user = ndb.IntegerProperty()
    title = ndb.StringProperty()
    slug = ndb.StringProperty()

    # class methods (ordered by alphabet)
    @classmethod
    def create(cls, id_workspace, id_user, title, slug):
        with client.context():
            # check if there's any entries with the same data already
            id_check = cls.query(cls.id_workspace == id_workspace, cls.id_user == id_user, cls.title == title, cls.slug == slug).get()

            if not id_check:  # if entry does not yet exist, create one

                # create the workspace object and store it into Datastore
                workspace_user = cls(id_workspace=id_workspace, id_user=id_user, title=title, slug=slug)
                workspace_user.put()

                return True, workspace_user, "Success"  # succes, workspace, message
            else:
                return False, None, "Workspace and user relation is already created. Please try again with new workspace and user."

    @classmethod
    def fetch(cls, limit=None, cursor=None):
        with client.context():
            workspaces, next_cursor, more = cls.query(WorkspaceUser.id_user == User.get_id).fetch_page(limit, start_cursor=cursor)

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
