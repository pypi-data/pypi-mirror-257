import os
import sys
import pathlib
import shutil
import time
import polars
import datetime
import pandas
import matplotlib.pyplot as plt
import typing
import warnings

sys.path.insert(0, '../src/FinToolsAP/')

import LocalDatabase
import Decorators
import LaTeXBuilder

# set printing options
pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)
pandas.set_option('display.width', shutil.get_terminal_size()[0])
pandas.set_option('display.float_format', lambda x: '%.3f' % x)

warnings.simplefilter(action = 'ignore', category = FutureWarning)

# directory for loacl wrds database 

# linux
LOCAL_WRDS_DB = pathlib.Path('/home/andrewperry/Documents')

@Decorators.Performance
def query_CRSP_performance(DB):
    return(DB.queryDB(DB.DBP.CRSP.CRSP_M, start_date = '2020-01-01', return_type = 'polars', suppress = True))

def group_nunique(df: polars.DataFrame | pandas.DataFrame, 
                  gr: str | list[str], 
                  vr: str | list[str], 
                  wt: typing.Optional[str] = None,
                  return_nan: typing.Optional[bool] = False,
                  name: typing.Optional[typing.Union[str, dict[str, str]]] = None, 
                  no_merge: typing.Optional[bool] = False, 
                  merge_how: typing.Optional[str] = 'left'
                ) -> polars.DataFrame | pandas.DataFrame:
        
        # type check df
        is_pandas = isinstance(df, pandas.DataFrame)
        if(not (is_pandas or isinstance(df, polars.DataFrame))):
            raise TypeError(f'df: expected type pandas.DataFrame or polars.DataFrame, got {type(df).__name__!r}')
        
        # type check gr
        if(not (isinstance(gr, str) or isinstance(gr, list))):
            raise TypeError(f'gr: expected type str or list[str], got {type(df).__name__!r}')
        
        # tpye check vr
        if(isinstance(gr, list)):
            if(not all(isinstance(x, str) for x in gr)):
                return TypeError(f'gr: expected a list of only strings, got {type(gr).__name__!r}')
            
        # type check vr
        if(not (isinstance(vr, str) or isinstance(vr, list))):
            raise TypeError(f'gr: expected type str or list[str], got {type(vr).__name__!r}')
            
        if(isinstance(vr, list)):
            if(not all(isinstance(x, str) for x in vr)):
                return TypeError(f'gr: expected a list of only str, got {type(vr).__name__!r}')
            
        if(isinstance(vr, str)):
            vr = [vr]
        
        # tpye check name
        if(name is not None):
            if(not (isinstance(name, str) or isinstance(name, dict))):
                raise TypeError(f'name: expected type str or dict[str:str], got {type(name).__name__!r}')
            
            if(isinstance(name, dict)):
                if(not all(isinstance(x, str) for x in name.keys())):
                    return TypeError(f'name: expected all keys of type str, got {type(name).__name__!r}')
                if(not all(isinstance(x, str) for x in name.values())):
                    return TypeError(f'name: expected all values of type str, got {type(name).__name__!r}')

        # type check no_merge     
        if(not isinstance(no_merge, bool)):
            raise TypeError(f'no_merge: expected type bool, got {type(no_merge).__name__!r}')

        names = {}
        if(isinstance(name, str)):
            # append name to column names in vr
            for col in vr:
                names[col] = f'{col}{name}'
        else:
            names = name

        res = df.group_by(gr).agg(polars.col(vr).n_unique())
        if(name is not None):
            res = res.rename(mapping = names)

        if(no_merge):
            return(res)
        else:
            if(is_pandas):
                res = df.merge(res, how = merge_how, on = gr)
            else:
                res = df.join(res, how = merge_how, on = gr)
            return(res)
                       


def main():

    DB = LocalDatabase.LocalDatabase(save_directory = LOCAL_WRDS_DB, 
                                     database_name = 'LCLDB'
                                    )

    df = query_CRSP_performance(DB)

    df = group_nunique(df, gr = 'exchcd', vr = 'permno', name = '_cnt')
    print(df.head())

    
    

if __name__ == "__main__":
    main()
