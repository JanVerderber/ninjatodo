from flask import request, redirect, url_for, abort

from models.workspace import Workspace
from models.workspace_user import WorkspaceUser
from models.user import User
from utils.decorators import login_required, set_csrf, validate_csrf
from utils.translations import render_template_with_translations
from datetime import date
from google.cloud.ndb import Cursor

@login_required
@set_csrf
def workspaces_list_handler(**params):
    cursor_arg = request.args.get('cursor')

    if cursor_arg:
        cursor = Cursor(urlsafe=cursor_arg.encode())
    else:
        cursor = None

    user = params["user"]
    user_id = user.get_id

    params["workspaces"], params["next_cursor"], params["more"] = WorkspaceUser.fetch(limit=None, cursor=cursor, user=user_id)

    if not cursor_arg:
        # normal browser get request
        return render_template_with_translations("profile/workspace/workspaces-list.html", **params)

@login_required
@validate_csrf
def workspace_create(**params):
    if request.method == "POST":
        title = request.form.get("title")
        slug = request.form.get("slug")
        date_raw = date.today()
        created_date = date_raw.strftime("%d %b %Y")
        user = params["user"]
        user_id = user.get_id

        if title and slug:
            result, workspace, message = Workspace.create(title=title, slug=slug, created_date=created_date, date_raw=date_raw)
            workspace_id = workspace.get_id

            if workspace:
                WorkspaceUser.create(id_workspace=workspace_id, id_user=user_id, title=title, slug=slug, created_date=created_date, date_raw=date_raw)

                return redirect(url_for("profile.workspace.workspaces_list_handler"))

        else:
            return abort(403, description="Please enter title and slug")
