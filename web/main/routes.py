from flask import redirect, url_for, render_template

from . import bp
from ..tools.commits import history_df, hours_per_day


@bp.route("/")
def index():
    return redirect(url_for("main.commits", project_name="calipso"))


@bp.route("/commits/<project_name>", methods=["GET"])
def commits(project_name):
    hits_df = hours_per_day(project_name)
    return render_template("commits.html", hits=hits_df.to_html())
