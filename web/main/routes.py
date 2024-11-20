
from flask import redirect, url_for, render_template

from . import bp
from ..tools.histories import repo_to_df, hours_per_day, merge_histories


@bp.route("/")
def index():
    return redirect(url_for("main.commits", project_name="calipso"))


@bp.route("/commits/<project_name>", methods=["GET"])
def commits(project_name):
    from datetime import datetime, timedelta
    later_date = datetime.now()
    sooner_date = later_date - timedelta(days=120)
    hits_df = merge_histories(project_name).truncate(before=sooner_date, after=later_date)
    return render_template("commits.html", hits=hits_df.to_html())
