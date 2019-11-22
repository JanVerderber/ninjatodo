from flask import request, redirect, url_for, abort

from models.workspaces import Workspace
from models.user import User
from utils.decorators import login_required, set_csrf, validate_csrf
from utils.translations import render_template_with_translations

@login_required
@set_csrf
def workspaces_list_handler(**params):
    if request.method == "GET":
        return render_template_with_translations("profile/main/workspaces.html", **params)

@login_required
@validate_csrf
def workspace_create(**params):
    if request.method == "POST":
        title = request.form.get("title")
        slug = request.form.get("slug")

        if title and slug:
            Workspace.create(title=title, slug=slug)

            return redirect(url_for("profile.workspaces.workspaces_list_handler"))

        else:
            return abort(403, description="Please enter title and slug")
