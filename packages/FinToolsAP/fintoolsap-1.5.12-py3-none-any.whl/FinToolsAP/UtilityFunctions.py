from __future__ import annotations

# standard imports
import typing
import polars
import pandas

def group_nunique(df: polars.DataFrame | pandas.DataFrame, 
                  gr: str | list[str], 
                  vr: str | list[str], 
                  name: typing.Optional[typing.Union[str, dict[str, str]]] = None, 
                  no_merge: typing.Optional[bool] = False, 
                  merge_how: typing.Optional[str] = 'left'
                ) -> polars.DataFrame | pandas.DataFrame:
        """
        Group by specified columns and calculate the number of unique values for each group.

        Parameters:
            df (polars.DataFrame or pandas.DataFrame): Input DataFrame.
            gr (str or list[str]): Grouping column(s).
            vr (str or list[str]): Column(s) on which to calculate the number of unique values.
            name (str or dict[str, str], optional): Custom name(s) for the resulting columns. 
                If a string is provided, it will be appended to the column names specified in `vr`.
                If a dictionary is provided, it should map original column names to new names.
                Defaults to None.
            no_merge (bool, optional): Whether to merge the result back to the original DataFrame. 
                on `gr`. Defaults to False.
            merge_how (str, optional): Method of merging if `no_merge` is False. 
                Possible values: 
                    Pandas: {`left`, `inner`, `outer`, `cross`, `right`}
                    Polars: {`left`, `inner`, `outer`, `cross`, `asof`, `semi`, `anti`}
                Defaults to 'left'.

        Returns:
            polars.DataFrame or pandas.DataFrame: DataFrame with the grouped results.

        Raises:
            TypeError: If input `df` is not a pandas.DataFrame or polars.DataFrame.
            TypeError: If input `gr` is not a string or a list of strings.
            TypeError: If input `vr` is not a string or a list of strings.
            TypeError: If input `name` is not a string, a dictionary with string keys and string values, or None.
            TypeError: If input `no_merge` is not a boolean.
        """
        
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

        if(is_pandas):
            res = df.groupby(by = gr)[vr].nunique()
            res = res.reset_index(drop = False)
            if(name is not None):
                res = res.rename(columns = names)
        else:
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