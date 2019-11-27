from google.cloud import ndb
from models import get_db


client = get_db()


class WorkspaceUser(ndb.Model):
    id_workspace = ndb.IntegerProperty()
    id_user = ndb.IntegerProperty()

    # class methods (ordered by alphabet)
    @classmethod
    def create(cls, id_workspace, id_user):
        with client.context():
            # check if there's any entries with the same data already
            id_check = cls.query(cls.id_workspace == id_workspace, cls. id_user == id_user).get()

            if not id_check:  # if entry does not yet exist, create one

                # create the workspace object and store it into Datastore
                workspace_user = cls(id_workspace=id_workspace, id_user=id_user)
                workspace_user.put()

                return True, workspace_user, "Success"  # succes, workspace, message
            else:
                return False, None, "Workspace and user relation is already created. Please try again with new workspace and user."
