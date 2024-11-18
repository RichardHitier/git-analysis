from flask import redirect, url_for, render_template

from . import bp


@bp.route("/")
def index():
    return redirect(url_for("main.commits"))


@bp.route("/commits")
def commits():
    return render_template("commits.html")
