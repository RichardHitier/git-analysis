from web.tools.histories import repo_to_df, hours_per_day, pomofocus_to_df, merge_histories, project_to_git_df


def test_repo_to_df():
    project_git_dir = "/home/richard/01DEV/CalipsoProject/calipso-dispatcher-clients/.git"
    df = repo_to_df(project_git_dir)
    print(df.head(20))
    assert True


def test_project_to_git_df():
    df = project_to_git_df("calipso")
    print(df)
    assert True


def test_hours_per_day():
    df = hours_per_day("calipso")
    print(df)
    # assert len(df) == 58
    assert True


def test_pomofocus_to_df():
    df = pomofocus_to_df("calipso")
    print(df)
    # assert len(df) == 58
    assert True


def test_merge_histories():
    df = merge_histories("calipso")
    import pandas as pd
    pd.set_option('display.max_rows', None)
    print(df.head())
    # print(df)
    assert True
