import pandas as pd


def join_dataframes(dataframes, cols, d):
    # Join all the dataframes from the same date to get one row per date.
    # Left dataframe cannot have empty columns.
    join_cols = [cols[0], cols[1]]
    if not dataframes[0].empty:
        # joined_dataframe = pd.merge(pd.merge(dataframes[0], dataframes[1], how='outer', on=[
        #     cols[0], cols[1]]), dataframes[2], how='outer', on=[cols[0], cols[1]])
        joined_df = pd.merge(
            dataframes[0], dataframes[1], how='outer', on=join_cols)
        joined_df = pd.merge(
            joined_df, dataframes[2], how='outer', on=join_cols)
    elif not dataframes[1].empty:
        print(f'df1 was empty. df2 not empty. date:{d}')
        # Need to insert empty columns at index 2 and 3.
        for i in range(2, 4):
            dataframes[1].insert(i, cols[i], pd.Series([]))
        joined_df = pd.merge(
            dataframes[1], dataframes[2], how='outer', on=join_cols)
    elif not dataframes[2].empty:
        print(f'df1 and d2 were empty. date:{d}')
        # Need to insert empty column at index 2, 3, 4, and 5.
        for i in range(2, 4):
            dataframes[2].insert(i, cols[i], pd.Series([]))
        joined_df = dataframes[2]
    else:
        print(f'all df were empty. date:{d}')
        joined_df = pd.DataFrame()
    return joined_df


def join_mlb_dataframes(dataframes, cols, d):
    # Join all the dataframes from the same date to get one row per date.
    # Left dataframe cannot have empty columns.
    join_cols = [cols[0], cols[1], cols[2], cols[3]]
    if not dataframes[0].empty:
        # joined_dataframe = pd.merge(pd.merge(dataframes[0], dataframes[1], how='outer', on=[
        #     cols[0], cols[1]]), dataframes[2], how='outer', on=[cols[0], cols[1]])
        joined_df = pd.merge(
            dataframes[0], dataframes[1], how='outer', on=join_cols)
        joined_df = pd.merge(
            joined_df, dataframes[2], how='outer', on=join_cols)
    elif not dataframes[1].empty:
        print(f'df1 was empty. df2 not empty. date:{d}')
        # Need to insert empty columns at index 4 and 5.
        for i in range(4, 6):
            dataframes[1].insert(i, cols[i], pd.Series([]))
        joined_df = pd.merge(
            dataframes[1], dataframes[2], how='outer', on=join_cols)
    elif not dataframes[2].empty:
        print(f'df1 and d2 were empty. date:{d}')
        # Need to insert empty column at index 4, 5, 6, and 7.
        for i in range(4, 8):
            dataframes[2].insert(i, cols[i], pd.Series([]))
        joined_df = dataframes[2]
    else:
        print(f'all df were empty. date:{d}')
        joined_df = pd.DataFrame()
    return joined_df
