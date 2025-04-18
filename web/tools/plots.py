import pandas as pd
import matplotlib.dates as mdates
from matplotlib import pyplot as plt

from datetime import date, timedelta

from web.tools.histories import merge_histories, pomo_minutes, pomofocus_to_df


def plot_df(_df):
    date_format = '%d %b'

    # get current month day
    today = date.today()

    month_before = today - timedelta(days=65)
    month_after = today + timedelta(days=30)

    pd_dr = pd.date_range(start=month_before, end=month_after, freq="D")

    _df = _df.reindex(pd_dr)

    fig, ax = plt.subplots(3, figsize=(20, 8), sharex=True)

    # ax[0].tick_params(axis='x', labelsize=10, rotation=30)
    # ax[2].xaxis.set_major_formatter(mdates.DateFormatter(date_format))
    # ax[2].tick_params(axis='x', labelsize=10, rotation=30)
    # ax[1].tick_params(axis='x', labelsize=10, rotation=30)
    # ax[2].set_xticks(pd_dr)

    try:
        ax[0].set_title("Number of Commits per day")
        bc = ax[0].bar(pd_dr, _df.nb_commits, color="red", width=0.8, edgecolor="black")
    except AttributeError:
        pass

    try:
        ax[1].set_title("Worked hours per day")
        cbc = ax[1].bar(pd_dr, _df.duration_hour, color="blue", width=0.8, edgecolor="black")
    except AttributeError:
        pass

    try:
        ax[2].set_title("Pomodoros per day")
        pbc = ax[2].bar(pd_dr, _df.minutes, width=0.5)
    except AttributeError:
        pass

    return fig


def pom_plot(_df):
    projects = [p.lower() for p in _df.main_project.unique() if p != '']

    fig, axs = plt.subplots(len(projects),
                            figsize=(20, 8),
                            sharex=True,
                            sharey=True)

    for i, p in enumerate(projects):
        ax = axs[i]
        ax.set_title(f"Project: {p}", y=1.1, pad=-25.0, loc="center")
        p_df = pomo_minutes(p, _df)
        pbc = ax.bar(p_df.index, p_df, width=0.5)

    return fig, projects


if __name__ == "__main__":
    # df = merge_histories("pro")
    pom_df = pomofocus_to_df()
    # print(pom_df.minutes)
    # _df = pomo_minutes("bht", pom_df)

    # my_fig = plot_df(_df)

    my_fig, p_l = pom_plot(pom_df)
    # my_fig.show()

    plt.show()
