from web.tools.histories import history_df, hours_per_day, pomofocus_to_df, merge_histories


def test_history_df():
    project_git_dir = "/home/richard/01DEV/CalipsoProject/calipso-dispatcher-clients/.git"
    df = history_df(project_git_dir)
    # import pandas as pd
    # pd.set_option('display.max_rows', None)
    print(df.head(20))
    # assert len(df) == 2389
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
    # print(df.tail())
    import pandas as pd
    pd.set_option('display.max_rows', None)
    print(df)
    assert True