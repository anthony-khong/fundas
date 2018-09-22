from functools import reduce

import pandas as pd

def select(*columns):
    columns = [columns] if isinstance(columns, str) else columns
    return lambda df: df[list(columns)]

def filter(predicate):
    return lambda df: df[predicate(df)].reset_index()

def with_column(new_column, column_fn):
    return lambda df: df.assign(**{new_column: column_fn(df)})

def with_columns(col_lambda_pairs):
    return lambda df: (
        df.assign(**{c: f(df) for c, f in col_lambda_pairs.items()}))

def with_column_renamed(old_column, new_column):
    return lambda df: df.rename(columns={old_column: new_column})

def with_columns_renamed(old_new_pairs):
    return lambda df: df.rename(columns=old_new_pairs)

def apply(fn):
    return lambda df: fn(df)

def join(right, on, how):
    return lambda df: df.merge(right, on=on, how=how)

def pipe(df, stages):
    return reduce(lambda df_so_far, stage: stage(df_so_far), stages, df)

def drop_columns(*columns):
    return lambda df: df.drop(columns=list(columns))

def groupby_agg(by, aggregators):
    apply = lambda grouped: pd.Series({
        column: agg_fn(grouped)
        for column, agg_fn in aggregators.items()
        })
    return lambda df: df.groupby(by).apply(apply).reset_index()

# TODO: def groupby_apply

def order_by(by, desc=False):
    return lambda df: df.sort_values(by=by, ascending=not desc).reset_index()
