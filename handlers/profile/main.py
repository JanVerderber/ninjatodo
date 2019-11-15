from flask import request, redirect, url_for

from models.user import User
from models.workspaces import Workspace
from utils.decorators import login_required, set_csrf, validate_csrf
from utils.translations import render_template_with_translations


@login_required
@set_csrf
def sessions_list(**params):
    if request.method == "GET":
        return render_template_with_translations("profile/main/sessions_list.html", **params)


@login_required
@validate_csrf
def session_delete(**params):
    if request.method == "POST":
        token_hash_five_chars = request.form.get("delete-session-token")
        User.delete_session(user=params["user"], token_hash_five_chars=token_hash_five_chars)

        return redirect(url_for("profile.main.sessions_list"))


@login_required
@set_csrf
def workspaces(**params):
    if request.method == "GET":
        return render_template_with_translations("profile/main/workspaces.html", **params)

    elif request.method == "POST":
        title = request.form.get("title")
        slug = request.form.get("slug")

        if title and slug:
            success, workspace, message = Workspace.create(title=title, slug=slug)

            if success:
                return render_template_with_translations("profile/main/workspaces.html", **params)
            else:
                params["register_error_message"] = message
                return render_template_with_translations("profile/main/workspaces.html", **params)
