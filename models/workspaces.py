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

                return "Success"  # succes, workspace, message
            else:
                return "Workspace with this slug is already created. Please try again with new slug."
