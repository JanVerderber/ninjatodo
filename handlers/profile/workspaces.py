from flask import request, redirect, url_for, abort

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

            return redirect(url_for("profile.main.workspaces"))

        else:
            return abort(403, description="Please enter title and slug")
