def select(columns):
    columns = [columns] if isinstance(columns, str) else columns
    return lambda df: df[columns]

def filter(predicate):
    return lambda df: df[predicate(df)].reset_index()
