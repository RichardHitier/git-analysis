import base64
from io import BytesIO

from dateutil import parser
from flask import redirect, url_for, render_template, request

from . import bp
from ..tools.histories import merge_histories, pomofocus_to_df
from ..tools.plots import plot_df, pom_plot


@bp.route("/")
def index():
    return redirect(url_for("main.commits", project_name="calipso"))


@bp.route("/commits/<project_name>", methods=["GET"])
def commits(project_name):
    from datetime import datetime, timedelta
    not_before = request.args.get('not_before')
    not_after = request.args.get('not_after')
    if not_after is None:
        later_date = datetime.now()
    else:
        later_date = parser.parse(not_after)
    if not_before is None:
        sooner_date = later_date - timedelta(days=60)
    else:
        sooner_date = parser.parse(not_before)
    hits_df = merge_histories(project_name)
    hits_df = hits_df.truncate(before=sooner_date, after=later_date)
    hits_fig = plot_df(hits_df)
    buf = BytesIO()
    hits_fig.savefig(buf, format="png")
    # Embed the result in the html output.
    img_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template("commits.html", hits=hits_df.to_html(), img_data=img_data)


@bp.route("/projects")
def projects():
    pom_df = pomofocus_to_df()
    buf = BytesIO()
    my_fig, p_l = pom_plot(pom_df)
    my_fig.savefig(buf, format="png")
    img_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template("projects.html", projects=p_l, img_data=img_data)
