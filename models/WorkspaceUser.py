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
            workspace_id_check = cls.query(cls.id_workspace == id_workspace).get()
            user_id_check = cls.query(cls.id_user == id_user).get()

            if not workspace_id_check and user_id_check:  # if entry does not yet exist, create one

                # create the workspace object and store it into Datastore
                workspace_user = cls(id_workspace=id_workspace, id_user=id_user)
                workspace_user.put()

                return "Success"  # succes, workspace, message
            else:
                return "Workspace and user relation is already created. Please try again with new workspace and user."
