import pandas as pd

import matplotlib

matplotlib.use("Agg")  # <- backend non-GUI
from matplotlib import pyplot as plt

from datetime import date, timedelta, datetime

from web.tools.histories import pomo_minutes, pomofocus_to_df, super_hours, superprod_to_df, merge_all_histories
from config import load_config, load_projects


def plot_df(_df):

    fig, ax = plt.subplots(4, figsize=(20, 8), sharex=True)

    try:
        ax[0].set_title("Git Commits per day")
        ax[0].set_ylim([-5, 30])
        ax[0].plot(_df.index, _df.git_commits.interpolate(method="spline", order=3), color="#bf0a30", lw=2, zorder=-4)
        ax[0].scatter(_df.index, _df.git_commits, marker="*", zorder=3, color="lightgreen", edgecolor="black", lw=0.5, s=50)
        # cbc = ax[0].bar(_df.index, _df.git_commits, color="#0f52ba", width=0.6, edgecolor="black")
    except AttributeError:
        pass

    try:
        ax[1].set_title("Git hours per day")
        hbc = ax[1].bar(_df.index, _df.git_hours, color="#bf0a30", width=0.6, edgecolor="black")
    except AttributeError:
        pass

    try:
        ax[2].set_title("Pomodoros per day")
        pbc = ax[2].bar(_df.index, _df.pomo_minutes, color="#89cfef", width=0.6, edgecolor="black")
    except AttributeError:
        pass

    try:
        ax[3].set_title("Super-productivity hours")
        sbc = ax[3].bar(_df.index, _df.super_hours, color="#fee12b", width=0.6, edgecolor="#3e424b")
        sbc = ax[3].bar(_df.index, _df.web_hours, color="#ffd6ff", width=0.6, edgecolor="#3e424b")
    except AttributeError:
        pass

    today = datetime.now().date()
    for i in range(4):
        ax[i].axvline(x=today, color='red', linestyle='--', linewidth=1)

    return fig


def all_plot(all_projects_df):
    projects = load_projects()

    fig, axs = plt.subplots(len(projects),
                            figsize=(20, 8),
                            sharex=True,
                            sharey=True)

    for i, project_name in enumerate(projects):
        ax = axs[i]
        ax.set_title(f"Project: {project_name}", y=1.1, pad=-25.0, loc="center")
        ax.set_ylabel("minutes")
        project_df = all_projects_df[all_projects_df['project'] == project_name]
        g_df = project_df.git_commits
        p_df = project_df.pomo_minutes
        s_df = project_df.super_hours * 60
        w_df = project_df.web_hours * 60

        ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
        ax2.set_ylim([-5, 30])
        ax2.plot(g_df.index, g_df.interpolate(method="spline", order=3), color="#bf0a30", lw=2, zorder=-4)
        ax2.scatter(g_df.index, g_df, marker="*", zorder=3, color="lightgreen", edgecolor="black", lw=0.5, s=50)

        pbc = ax.bar(p_df.index, p_df, width=0.5, color='#89cfef', label='Pomodoro', edgecolor="black", linewidth=0.2)
        sbc = ax.bar(s_df.index, s_df, width=0.5, color='#fee12b', label='Super', edgecolor="black", linewidth=0.2)
        wbc = ax.bar(w_df.index, w_df, width=0.5, color='#ffd6ff', label='Web', edgecolor="black", linewidth=0.2)
        today = datetime.now().date()
        ax.axvline(x=today, color='red', linestyle='--', linewidth=1)

    return fig, projects


if __name__ == "__main__":
    pomofocus_file = load_config()["POMOFOCUS_FILEPATH"]
    pom_df = pomofocus_to_df(pomofocus_file)
    superprod_file = load_config()["SUPERPROD_FILEPATH"]
    super_df = superprod_to_df(superprod_file)
    webprod_file = load_config()["WEBPROD_FILEPATH"]
    web_df = superprod_to_df(webprod_file)

    all_df = merge_all_histories(pom_df, super_df, web_df)
    all_df = all_df.truncate(before='20250101')
    my_fig, p_l = all_plot(all_df)
    # my_fig, p_l = pom_plot(pom_df, super_df, web_df)

    # plt.show()
    image_filename = "all_projects_2025.png"
    my_fig.savefig(image_filename)
    print(f"Saved to {image_filename}")
