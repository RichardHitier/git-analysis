import base64
from io import BytesIO

import pandas as pd
from dateutil import parser
from flask import redirect, url_for, render_template, request

from . import bp
from ..tools.histories import merge_histories, pomofocus_to_df, superprod_to_df, merge_all_histories
from ..tools.plots import plot_df, pom_plot, all_plot
from config import load_config


@bp.route("/")
def index():
    return redirect(url_for("main.projects"))


def sooner_or_later(request):
    from datetime import datetime, timedelta
    not_before = request.args.get('not_before')
    not_after = request.args.get('not_after')
    if not_after is None:
        later_date = datetime.now() + timedelta(days=10)
    else:
        later_date = parser.parse(not_after)
    if not_before is None:
        sooner_date = later_date - timedelta(days=120)
    else:
        sooner_date = parser.parse(not_before)
    sooner_date = datetime.date(sooner_date)
    later_date = datetime.date(later_date)
    return sooner_date, later_date


@bp.route("/commits/<project_name>", methods=["GET"])
def commits(project_name):
    pomofocus_file = load_config()["POMOFOCUS_FILEPATH"]
    superprod_file = load_config()["SUPERPROD_FILEPATH"]
    sooner_date, later_date = sooner_or_later(request)
    hits_df = merge_histories(project_name, pomofocus_file, superprod_file)
    hits_df = hits_df.truncate(before=sooner_date, after=later_date)
    new_index = pd.date_range(start=sooner_date, end=later_date, freq='D')
    hits_df = hits_df.reindex(new_index)
    hits_df.fillna(0.0, inplace=True)
    hits_fig = plot_df(hits_df)
    buf = BytesIO()
    hits_fig.savefig(buf, format="png")
    # Embed the result in the html output.
    img_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template("commits.html", hits=hits_df.to_html(), img_data=img_data)


@bp.route("/projects")
def projects():
    pomofocus_file = load_config()["POMOFOCUS_FILEPATH"]
    pom_df = pomofocus_to_df(pomofocus_file)
    superprod_file = load_config()["SUPERPROD_FILEPATH"]
    super_df = superprod_to_df(superprod_file)
    webprod_file = load_config()["WEBPROD_FILEPATH"]
    web_df = superprod_to_df(webprod_file)

    sooner_date, later_date = sooner_or_later(request)

    all_df = merge_all_histories(pom_df, super_df, web_df)
    all_df = all_df.truncate(before=sooner_date, after=later_date)
    my_fig, p_l = all_plot(all_df)
    # my_fig, p_l = pom_plot(pom_df, super_df, web_df)
    buf = BytesIO()
    my_fig.savefig(buf, format="png")
    img_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template("projects.html", projects=p_l, img_data=img_data)
