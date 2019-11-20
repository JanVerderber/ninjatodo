from flask import request

from models.workspaces import Workspace
from utils.decorators import login_required, set_csrf

@login_required
@set_csrf
def workspace_create(**params):
    if request.method == "POST":
        title = request.form.get("title")
        slug = request.form.get("slug")

        if title and slug:
            success, workspace, message = Workspace.create(title=title, slug=slug)

            return True, success, "Success"  # succes message
