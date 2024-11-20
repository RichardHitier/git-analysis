import pandas as pd
import matplotlib.dates as mdates
from matplotlib import pyplot as plt

from datetime import date, timedelta

from web.tools.histories import merge_histories


def plot_df(df):
    date_format = '%d %b'

    # get current month day
    today = date.today()

    month_before = today - timedelta(days=60)
    month_after = today + timedelta(days=30)

    pd_dr = pd.date_range(start=month_before, end=month_after, freq="D")

    df = df.reindex(pd_dr)

    fig, ax = plt.subplots(3, figsize=(20, 8), sharex=True)

    ax[0].tick_params(axis='x', labelsize=10, rotation=30)

    try:
        ax[0].xaxis.set_major_formatter(mdates.DateFormatter(date_format))
        ax[0].set_title("Number of Commits per day")
        bc = ax[0].bar(pd_dr, df.nb_commits, color="red", width=0.8, edgecolor="black")
    except AttributeError:
        pass

    try:
        ax[1].tick_params(axis='x', labelsize=10, rotation=30)
        ax[1].xaxis.set_major_formatter(mdates.DateFormatter(date_format))
        ax[1].set_title("Worked hours per day")
        cbc = ax[1].bar(pd_dr, df.duration_hour, color="blue", width=0.8, edgecolor="black")
    except AttributeError:
        pass

    ax[2].tick_params(axis='x', labelsize=10, rotation=30)
    ax[2].xaxis.set_major_formatter(mdates.DateFormatter(date_format))
    ax[2].set_title("Pomodoros per day")
    ax[2].set_xticks(pd_dr)
    pbc = ax[2].bar(pd_dr, df.minutes, width=0.5)

    return fig


if __name__ == "__main__":
    df = merge_histories("pro")

    my_fig = plot_df(df)

    # my_fig.show()

    plt.show()