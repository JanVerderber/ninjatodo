from google.cloud import ndb
from models import get_db


client = get_db()


class Workspace(ndb.Model):
    title = ndb.StringProperty()
    slug = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

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

            if not workspace:  # if workspace does not yet exist, create one

                # create the workspace object and store it into Datastore
                workspace = cls(title=title, slug=slug)
                workspace.put()

                return True, workspace, "Success"  # succes, workspace, message
            else:
                return False, None, "Workspace with this slug is already created. Please try again with new slug."

    @classmethod
    def delete(cls, workspace):
        with client.context():
            workspace_db = Workspace.get_by_id(workspace)
            workspace_db.deleted = True  # this does NOT delete workspace from Datastore (just marks it as "deleted")
            workspace_db.put()

        return True

    @classmethod
    def update(cls, workspace, title, slug):
        with client.context():
            workspace_db = Workspace.get_by_id(workspace)
            workspace_db.title = title
            workspace_db.slug = slug
            workspace_db.put()

        return True
