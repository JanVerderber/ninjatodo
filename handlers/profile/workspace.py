from flask import request, redirect, url_for, abort

from models.workspace import Workspace
from models.workspace_user import WorkspaceUser
from models.user import User
from utils.decorators import login_required, set_csrf, validate_csrf
from utils.translations import render_template_with_translations
from google.cloud.ndb import Cursor

@login_required
@set_csrf
def workspaces_list_handler(**params):
    cursor_arg = request.args.get('cursor')

    if cursor_arg:
        cursor = Cursor(urlsafe=cursor_arg.encode())
    else:
        cursor = None

    params["workspaces"], params["next_cursor"], params["more"] = Workspace.fetch(limit=10, cursor=cursor)

    if not cursor_arg:
        # normal browser get request
        return render_template_with_translations("profile/workspace/workspaces-list.html", **params)

@login_required
@validate_csrf
def workspace_create(**params):
    if request.method == "POST":
        title = request.form.get("title")
        slug = request.form.get("slug")
        user = params["user"]
        user_id = user.get_id

        if title and slug:
            result, workspace, message = Workspace.create(title=title, slug=slug)
            workspace_id = workspace.get_id

            if workspace:
                WorkspaceUser.create(id_workspace=workspace_id, id_user=user_id)

                return redirect(url_for("profile.workspace.workspaces_list_handler"))

        else:
            return abort(403, description="Please enter title and slug")
