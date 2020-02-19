import logging

from flask import request, redirect, url_for, abort

from models.workspace import Workspace
from models.workspace_user import WorkspaceUser
from models.user import User
from models import get_db
from utils.decorators import login_required, set_csrf, validate_csrf
from utils.translations import render_template_with_translations
from google.cloud.ndb import Cursor

client = get_db()

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
@set_csrf
def users_list_handler(slug, **params):
    users_dicts = []
    with client.context():
        selected_workspace = WorkspaceUser.query(WorkspaceUser.slug == slug, WorkspaceUser.deleted == False).fetch()
        all_users = User.query().fetch()

    for workspace_user_info in selected_workspace:
        user = workspace_user_info.id_user
        user_obj = User.get_user_by_id(user)
        users_dicts.append({"user_id": user, "first_name": user_obj.first_name, "last_name": user_obj.last_name, "is_owner": workspace_user_info.is_owner,
                            "created": workspace_user_info.created, "id_workspace": workspace_user_info.id_workspace})

    params["workspace_users"] = users_dicts
    params["all_users"] = all_users

    return render_template_with_translations("profile/workspace/workspace-users-list.html", **params)

@login_required
@set_csrf
def delete(**params):
    if request.method == "POST":
        workspace_id = request.form.get("workspace-id")
        int_workspace = int(workspace_id)
        WorkspaceUser.delete(int_workspace)
        Workspace.delete(int_workspace)

        return redirect(url_for("profile.workspace.workspaces_list_handler"))

@login_required
@set_csrf
def remove_workspace_user(**params):
    if request.method == "POST":
        workspace_user_id = request.form.get("workspace-user-id")
        workspace_user_id = int(workspace_user_id)
        WorkspaceUser.delete_by_user(workspace_user_id)

        return redirect(url_for("profile.workspace.workspaces_list_handler"))  # FIX: Redirect to users list

@login_required
@set_csrf
def update(**params):
    if request.method == "POST":
        workspace_id = request.form.get("workspace-id")
        int_workspace = int(workspace_id)
        title = request.form.get("edit-title")
        WorkspaceUser.update(int_workspace, title)
        Workspace.update(int_workspace, title)

        return redirect(url_for("profile.workspace.workspaces_list_handler"))

@login_required
@validate_csrf
def workspace_create(**params):
    if request.method == "POST":
        title = request.form.get("title")
        slug = request.form.get("slug")
        add_user = request.form.get("add_user")  # True or False, if we want to add a user or create new workspace
        add_user_id = request.form.get("add_user_id")  # ID from the user that we want to add to workspace
        id_workspace = request.form.get("id_workspace")  # ID from workspace that we want to add user to
        is_owner = request.form.get("is-owner")
        user = params["user"]
        user_id = user.get_id

        if is_owner == "True":
            is_owner = True

        else:
            is_owner = False

        if add_user == "True":
            with client.context():
                if add_user_id and id_workspace:
                    add_user_id = int(add_user_id)
                    id_workspace = int(id_workspace)
                    workspace_user_info = WorkspaceUser.query(WorkspaceUser.id_workspace == id_workspace, WorkspaceUser.deleted == False).fetch(limit=1)
                    for x in workspace_user_info:
                        title = x.title
                        slug = x.slug

            WorkspaceUser.create(id_workspace=id_workspace, id_user=add_user_id, title=title, slug=slug, is_owner=is_owner)

            return redirect(url_for("profile.workspace.workspaces_list_handler"))  # FIX: Redirect to users list

        else:
            if title and slug:
                result, workspace, message = Workspace.create(title=title, slug=slug)
                workspace_id = workspace.get_id

                if workspace:
                    WorkspaceUser.create(id_workspace=workspace_id, id_user=user_id, title=title, slug=slug, is_owner=is_owner)

                    return redirect(url_for("profile.workspace.workspaces_list_handler"))

            else:
                return abort(403, description="Please enter title and slug")
