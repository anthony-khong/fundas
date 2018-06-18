from functools import reduce

def select(columns):
    columns = [columns] if isinstance(columns, str) else columns
    return lambda df: df[columns]

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

def pipe(df, stages):
    return reduce(lambda df_so_far, stage: stage(df_so_far), stages, df)
