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
