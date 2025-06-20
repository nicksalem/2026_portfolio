import pandas as pd
import numpy as np
import os
from typing import Tuple

def build_data_frame(data_directory:str) -> Tuple[pd.DataFrame, pd.DataFrame]:  
    """Build a data frame given a data directory
    
    Returns two dataframes
    """

    dataframes = []

    row_count = 0

    for dirpath, dirs, files in os.walk(data_directory):
        for n, file in enumerate(files):
            df = pd.read_csv(os.path.join(dirpath,file))
            df = df.drop('Player-additional', axis=1)
            df['Year'] = 2020 + n + 1
            if 'MP▼' in df.columns:
                df.rename(columns={'MP▼':'MP'}, inplace=True)

            if 'Team' in df.columns:
                df.rename(columns={'Team':'Tm'}, inplace=True) 

            dataframes.append(df)
            row_count += df.shape[0]

    nba_df = pd.concat(dataframes)

    #select columns of interest
    nba_totals = nba_df[['Player', 'Tm','Pos', 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', '3P',
       '3PA', '2P', '2PA', 'FT', 'FTA', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'Year']].copy()
    
    #drop the total rows to avoid double counting
    nba_totals = nba_totals[~(nba_totals['Tm'] == 'TOT') & ~(nba_totals['Tm'] == '2TM') & ~(nba_totals['Tm'] == '3TM')].copy()

    # if the data type is numeric return the sum if the data type is not then return the mode (Pos, Tm)
    def smart_agg(x):
        if np.issubdtype(x.dtype, np.number):
            return x.sum()
        else:
            return x.mode()[0]  # or .mode()[0], .unique(), etc.

    nba_totals_agg = nba_totals.groupby(['Player', 'Age', 'Year']).agg(lambda x: smart_agg(x)).reset_index()


    return nba_df, nba_totals_agg