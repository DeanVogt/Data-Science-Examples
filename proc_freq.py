import pandas as pd


def proc_freq(df, vars, dropna=False, sort_vars=False):
    """
    This function attempts to mimic basic SAS' PROC FREQ functionality.

    df should either be a pandas dataframe or a pandas-on-Spark dataframe.
    """
    temp_df = df.groupby(vars, dropna=dropna).size().reset_index(name='freq')
    
    if isinstance(temp_df, pd.DataFrame):
        pass
    else: 
        temp_df = temp_df.to_pandas()
    
    if sort_vars:
        temp_df = temp_df.sort_values(vars).reset_index(drop=True)
    else:
        temp_df = temp_df.sort_values('freq', ascending=False).reset_index(drop=True)
        
    temp_df['cum freq'] = temp_df['freq'].cumsum()
    temp_df['pct'] = temp_df['freq'] / df.shape[0] * 100
    temp_df['cum pct'] = temp_df['cum freq'] / df.shape[0] * 100
    temp_df['freq'] = temp_df['freq'].apply(lambda x: '{:,.0f}'.format(x))
    temp_df['cum freq'] = temp_df['cum freq'].apply(lambda x: '{:,.0f}'.format(x))
    temp_df['pct'] = temp_df['pct'].round(2)
    temp_df['cum pct'] = temp_df['cum pct'].round(2)
    
    return temp_df
