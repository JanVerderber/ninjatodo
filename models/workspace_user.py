import datetime

from google.cloud import ndb
from models import get_db


client = get_db()


class WorkspaceUser(ndb.Model):
    id_workspace = ndb.IntegerProperty()
    id_user = ndb.IntegerProperty()
    is_owner = ndb.BooleanProperty(default=False)
    title = ndb.StringProperty()
    slug = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    # class methods (ordered by alphabet)
    @classmethod
    def create(cls, id_workspace, id_user, title, slug, is_owner):
        with client.context():
            # check if there's any entries with the same data already
            id_check = cls.query(cls.id_workspace == id_workspace, cls.id_user == id_user).get()

            if not id_check:  # if entry does not yet exist, create one

                # create the workspace object and store it into Datastore
                workspace_user = cls(id_workspace=id_workspace, id_user=id_user, title=title, slug=slug, is_owner=is_owner)
                workspace_user.put()

                return True, workspace_user, "Success"  # succes, workspace, message
            else:
                return False, None, "Workspace and user relation is already created. Please try again with new workspace and user."

    @classmethod
    def fetch(cls, limit=None, cursor=None, user=None):
        with client.context():
            workspaces, next_cursor, more = cls.query(WorkspaceUser.id_user == user, cls.deleted == False).fetch_page(limit, start_cursor=cursor)

            if limit and len(workspaces) < limit:
                return workspaces, None, False

            try:
                return workspaces, next_cursor.urlsafe().decode(), more
            except AttributeError as e:  # if there's no next_cursor, an AttributeError will occur
                return workspaces, None, False

    @classmethod
    def fetch_by_slug(cls, limit=None, cursor=None, slug=None):
        with client.context():
            workspaces, next_cursor, more = cls.query(WorkspaceUser.slug == slug, cls.deleted == False).fetch_page(
                limit, start_cursor=cursor)

            if limit and len(workspaces) < limit:
                return workspaces, None, False

            try:
                return workspaces, next_cursor.urlsafe().decode(), more
            except AttributeError as e:  # if there's no next_cursor, an AttributeError will occur
                return workspaces, None, False

    @classmethod
    def fetch_by_id(cls, limit=None, cursor=None, id_workspace=None):
        with client.context():
            workspace_user, next_cursor, more = cls.query(WorkspaceUser.id_workspace == id_workspace, cls.deleted == False).fetch_page(
                limit, start_cursor=cursor)

            if limit and len(workspace_user) < limit:
                return workspace_user, None, False

            try:
                return workspace_user, next_cursor.urlsafe().decode(), more
            except AttributeError as e:  # if there's no next_cursor, an AttributeError will occur
                return workspace_user, None, False

    @classmethod
    def fetch_by_user_id(cls, limit=None, cursor=None, id_user=None):
        with client.context():
            workspace_user, next_cursor, more = cls.query(WorkspaceUser.id_user == id_user, cls.deleted == False).fetch_page(limit, start_cursor=cursor)

            if limit and len(workspace_user) < limit:
                return workspace_user, None, False

            try:
                return workspace_user, next_cursor.urlsafe().decode(), more
            except AttributeError as e:  # if there's no next_cursor, an AttributeError will occur
                return workspace_user, None, False

    @classmethod
    def delete(cls, workspace):
        with client.context():
            workspace_db = cls.query(cls.id_workspace == workspace).get()
            workspace_db.deleted = True  # this does NOT delete workspace from Datastore (just marks it as "deleted")
            workspace_db.put()

        return True

    @classmethod
    def delete_by_user(cls, user_id):
        with client.context():
            workspace_db = cls.query(cls.id_user == user_id).get()
            workspace_db.deleted = True  # this does NOT delete workspace from Datastore (just marks it as "deleted")
            workspace_db.put()

        return True

    @classmethod
    def update(cls, workspace, title):
        with client.context():
            workspace_db = cls.query(cls.id_workspace == workspace).get()
            workspace_db.title = title
            workspace_db.updated = datetime.datetime.now()
            workspace_db.put()

        return True
