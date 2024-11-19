from datetime import datetime, timedelta
import pandas as pd

import subprocess

projects = {
    # "calipso": {'git_dirs': ['/home/richard/01DEV/CalipsoProject/calipso-dispatcher-clients/.git',
    #                          '/home/richard/01DEV/CalipsoProject/calipso-dispatcher-studio-1/.git',
    #                          '/home/richard/01DEV/CalipsoProject/calipso-net-module/.git',
    #                          '/home/richard/01DEV/CalipsoProject/.git',
    #                          ]},
    "calipso": {'git_dirs': ['/home/richard/01DEV/CalipsoProject/calipso-dispatcher-clients/.git']},
    "bht": {'git_dirs': ['/home/richard/01DEV/bht2/.git']},
}


class ProjectError(Exception):

    def __init__(self, message="Git Analysis Error"):
        self.message = message
        super().__init__(self.message)


def history_df(project_git_dir):
    """ Build a dataframe with one row per commit
        and columns Date, Day, Hour, Nb_Commit
        So we can further run analysis, sums, and plot
    """

    # run git on repo: outputs commits timestamps
    gitlog_args = ['git', f'--git-dir={project_git_dir}', 'log', '--all', '--pretty="%at"']
    print(" ".join(gitlog_args))
    gitlog_out = subprocess.check_output(gitlog_args, stderr=subprocess.STDOUT)

    # transform to timestamp list
    gitlog_str_out = gitlog_out.decode("utf-8")
    gitlog_str_out = gitlog_str_out.replace('"', '')
    gitlog_str_list = gitlog_str_out.split('\n')

    # make the datas list
    timestamps_list = list(map(lambda x: int(x), gitlog_str_list[:-2]))
    date_list = list(map(lambda X: pd.to_datetime(X, unit="s"), timestamps_list))
    day_list = list(map(lambda X: datetime.strftime(X, "%Y-%m-%d"), date_list))
    hour_list = list(map(lambda X: datetime.strftime(X, "%H:%M:%S"), date_list))

    data = zip(date_list, day_list, hour_list)

    # and return pandas dataframe
    _df = pd.DataFrame(data, columns=["date", "day", "hour"])

    # create a new column with 1 (one) commit per timestamp row
    _df["nb_commits"] = 1

    return _df


def hours_per_day(project_name, sooner_date=None, later_date=None):
    """ From The git history dataframe,
        build a new serie with the number of hours worked each day.
        in fact, a delta between last and first commit time for each day.
    """

    if later_date is None:
        later_date = datetime.now()
    if sooner_date is None:
        sooner_date = (later_date - timedelta(days=120))

    if isinstance(later_date, datetime):
        later_date = later_date.strftime("%Y-%m-%d")
    if isinstance(sooner_date, datetime):
        sooner_date = sooner_date.strftime("%Y-%m-%d")

    # get the git history, raw
    if project_name not in projects.keys():
        raise (ProjectError(f"Wrong project name:{project_name}"))

    df_2 = pd.DataFrame(columns=['duration_hour', 'duration_day', ' project'])

    for project_git_dir in projects[project_name]['git_dirs']:
        df_1 = history_df(project_git_dir)
        df_2 = pd.concat([df_2, df_1])

    # day by day, get the min hour, and max hour
    df_3 = df_2.groupby("day").date.agg(["min", "max"])
    df_4 = df_3.copy()

    # day by day, get the duration, in hour (float) and day part (float)
    df_4["duration"] = df_4.apply(lambda x: x["max"] - x["min"], axis=1)
    df_4["duration_hour"] = df_4.apply(lambda x: f"{x['duration'].seconds / 3600:.02f}", axis=1)
    df_4["duration_day"] = df_4.apply(lambda x: f"{x['duration'].seconds / (3600 * 8):.03f}", axis=1)
    df_5 = df_4[["duration_hour", "duration_day"]].truncate(before=sooner_date, after=later_date)
    # df_5 = df_4[["duration_hour", "duration_day"]].truncate(before="2024-09-15")
    # df_5 = df_4[["duration_hour", "duration_day"]]
    df_5["project"] = project_name
    # print(df_5)
    df_5.index = pd.to_datetime(df_5.index)
    new_index = pd.date_range(start=df_5.index[0], end=df_5.index[-1])
    df_6 = df_5.reindex(new_index)
    df_6["duration_hour"] = df_6["duration_hour"].apply(lambda x: float(x))
    df_6["duration_day"] = df_6["duration_day"].apply(lambda x: float(x))

    return df_6
