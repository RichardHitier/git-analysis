from datetime import datetime, timedelta
import pandas as pd

import subprocess

from config import load_projects


class ProjectError(Exception):

    def __init__(self, message="Git Analysis Error"):
        self.message = message
        super().__init__(self.message)


def repo_to_df(project_git_dir):
    """ From a git repository (.git/ directory)
        build a dataframe with one row per commit
        with columns Date, Day, Hour, Nb_Commit
        so we can further run analysis, sums, and plot
    """

    # run git on repo: outputs commits timestamps
    gitlog_args = ['git', f'--git-dir={project_git_dir}', 'log', '--all', '--pretty="%at"']
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


def project_to_df(project_name):
    """From a project name, retrieve a list of repository
       and concatenate resulting dataframes
       see also:
        - :meth: `repo_to_df()`
    """
    projects = load_projects()
    # get the git history, raw
    if project_name not in projects.keys():
        raise (ProjectError(f"Wrong project name:{project_name}"))

    git_dfs = []

    for project_git_dir in projects[project_name]['git_dirs']:
        git_dfs.append(repo_to_df(project_git_dir))
    if len(git_dfs) == 0:
        res_df = None
    else:
        res_df = pd.concat(git_dfs)
    return res_df


def daily_commits(project_df):
    """ From the one commit per row dataframe,
        build a new dataframe, indexed by days, with sum of commits per day

        see also:
            - :meth: `project_to_df)`
    """

    project_df = project_df.copy()
    project_df.index = project_df.day
    # project_df.rename(columns={"nb_commits": "commits"}, inplace=True)
    project_df.drop(columns=["date", "hour", "day"], inplace=True)
    project_df.index = pd.to_datetime(project_df.index)

    groupby_key = "day"

    _df_agg = project_df.groupby(groupby_key).agg("sum")

    _df_agg.sort_values(groupby_key, inplace=True)

    start_date = _df_agg.index[0]
    end_date = _df_agg.index[-1]

    new_index = pd.date_range(start=start_date, end=end_date, freq="d")

    _df_reindexed = _df_agg.reindex(new_index)

    _df_cutted = _df_reindexed.truncate(before="2023-09-01")

    return _df_cutted


def hours_per_day(project_df):
    """ From The git history dataframe,
        build a new pd.series with the number of hours worked each day.
        in fact, a delta between last and first commit time for each day.

        see also:
            - :meth: `project_to_df)`
    """

    # day by day, get the min hour, and max hour
    project_df = project_df.copy()
    df_3 = project_df.groupby("day").date.agg(["min", "max"])
    df_4 = df_3.copy()

    # day by day, get the duration, in hour (float) and day part (float)
    df_4["duration"] = df_4.apply(lambda x: x["max"] - x["min"], axis=1)
    df_4["duration_hour"] = df_4.apply(lambda x: f"{x['duration'].seconds / 3600:.02f}", axis=1)
    df_4["duration_day"] = df_4.apply(lambda x: f"{x['duration'].seconds / (3600 * 8):.03f}", axis=1)
    df_5 = df_4[["duration_hour", "duration_day"]]
    # df_5["project"] = project_name
    df_5.index = pd.to_datetime(df_5.index)
    new_index = pd.date_range(start=df_5.index[0], end=df_5.index[-1])
    df_6 = df_5.reindex(new_index)
    df_6["duration_hour"] = df_6["duration_hour"].apply(lambda x: float(x))
    df_6["duration_day"] = df_6["duration_day"].apply(lambda x: float(x))

    return df_6


def pomofocus_to_df(pomofocus_file):
    """From a pomofocus exported file
       build the dataframe
    """
    _df = pd.read_csv(pomofocus_file, header=0, index_col=0, parse_dates=True)
    # read_excel("pomodoros.ods", sheet_name="pomodoros",header=1, index_col=0, parse_dates=True)
    _df.fillna(0, inplace=True)
    # 1- Insert new column 'main_project' keeping first part of project name
    _df.insert(0, 'main_project', "")
    _df['main_project'] = _df.project.apply(lambda x: x.split()[0] if x != 0 else "")

    return _df


def pomo_minutes(project_name, _my_df):
    """From the pomofocus data_frame
        extract given project minutes df
    """
    projects = load_projects()
    if project_name not in projects.keys():
        raise (ProjectError(f"Wrong project name:{project_name}"))

    pom_project = projects[project_name]['pom_project']

    # 2- extract wanted project only and keep only two columns
    _my_df = _my_df[_my_df['main_project'] == pom_project]
    _my_df = _my_df.minutes

    # 3- aggregate by day
    _my_df = _my_df.groupby(level=0).sum()

    # 4- add missing days reindex
    day_first = _my_df.index[0]
    day_last = _my_df.index[-1]
    day_idx = pd.date_range(start=day_first, end=day_last, freq='D')
    _my_df = _my_df.reindex(day_idx, fill_value=0.0)

    return _my_df


def merge_histories(project_name, pomofocus_file):
    """
    Merge git and pomodoro histories in one dataframe

    :param pomofocus_file:
    :param project_name:
    :return:
    """

    git_df = project_to_df(project_name)
    df_to_concat = []
    if git_df is not None:
        dly_df = daily_commits(git_df)
        df_to_concat.append(dly_df)
        hrs_df = hours_per_day(git_df)
        df_to_concat.append(hrs_df)
    minutes_df = pomo_minutes(project_name, pomofocus_to_df(pomofocus_file))
    df_to_concat.append(minutes_df)
    res_df = pd.concat(df_to_concat, axis=1)
    res_df.fillna(0.0, inplace=True)

    new_index = pd.date_range(start=res_df.index[0], end=res_df.index[-1])
    res_df = res_df.reindex(new_index)
    return res_df


if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
    available_options = ['pomofocus', 'pomo_bht', 'git_bht', 'merged_bht']
    import sys
    from config import load_config
    pomofocus_file = load_config()["POMOFOCUS_FILEPATH"]
    cli_arg = None
    if len(sys.argv) > 1:
        cli_arg = sys.argv[1]
    if cli_arg == 'pomofocus':
        print(pomofocus_to_df(pomofocus_file))
    elif cli_arg == 'git_all':
        print('gitall')
    elif cli_arg == 'pomo_bht':
        print(pomo_minutes('bht', pomofocus_to_df(pomofocus_file)))
    elif cli_arg == 'git_bht':
        print(project_to_df('bht'))
    elif cli_arg == 'merged_bht':
        print(merge_histories('bht', pomofocus_file))
    else:
        print(f"Pass option in [{', '.join(available_options)}]")