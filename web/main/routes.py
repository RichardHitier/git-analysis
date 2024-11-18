from flask import redirect, url_for, render_template

from . import bp
from ..tools import show_me


@bp.route("/")
def index():
    return redirect(url_for("main.commits", project_name="calipso"))


@bp.route("/commits/<project_name>", methods=["GET"])
def commits(project_name):
    hits = show_me(project_name)
    return render_template("commits.html", hits=hits)
