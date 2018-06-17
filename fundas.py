def select(columns):
    columns = [columns] if isinstance(columns, str) else columns
    return lambda df: df[columns]

def filter(predicate):
    return lambda df: df[predicate(df)].reset_index()

def with_column(new_column, column_fn):
    return lambda df: df.assign(**{new_column: column_fn(df)})
