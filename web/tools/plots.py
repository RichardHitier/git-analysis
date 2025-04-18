import pandas as pd
from matplotlib import pyplot as plt

from datetime import date, timedelta, datetime

from web.tools.histories import pomo_minutes, pomofocus_to_df, super_hours
from config import load_config, load_projects


def plot_df(_df):
    date_format = '%d %b'

    # get current month day
    today = date.today()

    month_before = today - timedelta(days=65)
    month_after = today + timedelta(days=30)

    pd_dr = pd.date_range(start=month_before, end=month_after, freq="D")

    _df = _df.reindex(pd_dr)

    fig, ax = plt.subplots(4, figsize=(20, 8), sharex=True)

    # ax[0].tick_params(axis='x', labelsize=10, rotation=30)
    # ax[2].xaxis.set_major_formatter(mdates.DateFormatter(date_format))
    # ax[2].tick_params(axis='x', labelsize=10, rotation=30)
    # ax[1].tick_params(axis='x', labelsize=10, rotation=30)
    # ax[2].set_xticks(pd_dr)

    try:
        ax[0].set_title("Git Commits per day")
        cbc = ax[0].bar(pd_dr, _df.nb_commits, color="#bf0a30", width=0.6, edgecolor="black")
    except AttributeError:
        pass

    try:
        ax[1].set_title("Git hours per day")
        hbc = ax[1].bar(pd_dr, _df.duration_hour, color="#0f52ba", width=0.6, edgecolor="black")
    except AttributeError:
        pass

    try:
        ax[2].set_title("Pomodoros per day")
        pbc = ax[1].bar(pd_dr, _df.minutes, color="#89cfef", width=0.6, edgecolor="black")
    except AttributeError:
        pass

    try:
        ax[3].set_title("Super-productivity hours")
        sbc = ax[3].bar(pd_dr, _df.super_hours, color="#fee12b", width=0.6, edgecolor="#3e424b")
    except AttributeError:
        pass

    today = datetime.now().date()
    for i in range(4):
        ax[i].axvline(x=today, color='red', linestyle='--', linewidth=1)

    return fig


def pom_plot(pom_df, super_df):
    projects = load_projects()

    fig, axs = plt.subplots(len(projects),
                            figsize=(20, 8),
                            sharex=True,
                            sharey=True)

    for i, project_name in enumerate(projects):
        ax = axs[i]
        ax.set_title(f"Project: {project_name}", y=1.1, pad=-25.0, loc="center")
        ax.set_ylabel("minutes")
        p_df = pomo_minutes(project_name, pom_df)
        s_df = super_hours(project_name, super_df)*60
        pbc = ax.bar(p_df.index, p_df, width=0.7, color='#89cfef', label='Pomodoro', edgecolor="black", linewidth=0.2)
        sbc = ax.bar(s_df.index, s_df, width=0.7, color='#fee12b', label='Super', edgecolor="black", linewidth=0.2)
        today = datetime.now().date()
        ax.axvline(x=today, color='red', linestyle='--', linewidth=1)

    return fig, projects


if __name__ == "__main__":
    # df = merge_histories("pro")
    pomofocus_file = load_config()["POMOFOCUS_FILEPATH"]
    pom_df = pomofocus_to_df(pomofocus_file)
    # print(pom_df.minutes)
    # _df = pomo_minutes("bht", pom_df)

    # my_fig = plot_df(_df)

    my_fig, p_l = pom_plot(pom_df)
    # my_fig.show()

    plt.show()
