import base64
from io import BytesIO

from flask import redirect, url_for, render_template

from . import bp
from ..tools.histories import merge_histories, pomofocus_to_df
from ..tools.plots import plot_df


@bp.route("/")
def index():
    return redirect(url_for("main.commits", project_name="calipso"))


@bp.route("/commits/<project_name>", methods=["GET"])
def commits(project_name):
    from datetime import datetime, timedelta
    later_date = datetime.now()
    sooner_date = later_date - timedelta(days=120)
    hits_df = merge_histories(project_name).truncate(before=sooner_date, after=later_date)
    hits_fig = plot_df(hits_df)
    buf = BytesIO()
    hits_fig.savefig(buf, format="png")
    # Embed the result in the html output.
    img_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template("commits.html", hits=hits_df.to_html(), img_data=img_data)


@bp.route("/projects")
def projects():
    pom_df = pomofocus_to_df()