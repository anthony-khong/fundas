import numpy as np
import pytest as pt

import pandas as pd
import fundas as fd

DF = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b': [1, 2, 3, 2, 1]})

def test_select():
    assert fd.select(['a'])(DF).columns == ['a'], (
            'Selected wrong column from a list')
    assert fd.select('b')(DF).columns == ['b'], (
            'Selected wrong column from a string')
    with pt.raises(KeyError):
        fd.select('c')(DF)

def test_filter():
    filtered = fd.filter(lambda x: x.a % 2 != 0)(DF)
    assert np.all(filtered.index == np.arange(len(filtered))), (
            'Filter messed up DataFrame index.')
    assert filtered.a.tolist() == [1, 3, 5], (
            'Filtered out wrong rows for same column.')
    assert filtered.b.tolist() == [1, 3, 1], (
            'Filtered out wrong rows for diff column.')

def test_between():
    filtered = fd.filter(lambda x: fd.between(x.b, 2, 3))(DF)
    assert filtered.a.tolist() == [2, 3, 4], 'Between function not correct.'

def test_with_column():
    assert (
        fd.with_column('c', lambda x: x.a + x.b)(DF).c.tolist()
        == [2, 4, 6, 6, 6]
        ), 'With-column makes wrong new column.'
    assert (
        fd.with_column('a', lambda x: x.a**2)(DF).a.tolist()
        == [1, 4, 9, 16, 25]
        ), 'With-column makes wrong new column.'
    assert DF.a.tolist() == [1, 2, 3, 4, 5], (
            'With-column makes a mutation.')

def test_with_columns():
    new_df = fd.with_columns({
        'a': lambda x: 1,
        'c': lambda x: x.a + x.b
        })(DF)
    new_df.a.tolist() == [2, 3, 4, 5, 6], (
            'With-columns does not change existing column.')
    new_df.c.tolist() == [2, 4, 6, 6, 6], (
            'With-columns does not change new column correctly.')

def test_with_column_renamed():
    renamed_df = fd.with_column_renamed('a', 'c')(DF)
    with pt.raises(KeyError):
        renamed_df['a']
    assert renamed_df.c.tolist() == DF.a.tolist(), (
            'With-column-renamed mutates original values.')

def test_with_columns_renamed():
    renamed_df = fd.with_columns_renamed({'a': 'A', 'b': 'B'})(DF)
    assert set(renamed_df) == {'A', 'B'}, (
            'With-columns-renamed do not rename correctly.')
    assert set(DF) == {'a', 'b'}, (
            'With-columns-renamed mutates original columns.')

def test_pipe():
    piped_df = fd.pipe(
            DF, [
            fd.filter(lambda x: x.a % 2 == 0),
            fd.with_column('c', lambda x: x.a + 1),
            fd.with_column_renamed('a', 'A'),
            fd.with_column('d', lambda x: x.A ** 2),
            fd.select(['A', 'b', 'c'])
            ])
    assert (
        (piped_df.A.tolist() == [2, 4])
        & (piped_df.c.tolist() == [3, 5])
        & (piped_df.b.tolist() == [2, 2])
        & (set(piped_df) == {'A', 'b', 'c'})
        ), 'Mistakes in piping.'

    other_piped_df = (
        fd.Pipe(DF)
          .filter(lambda x: x.a % 2 == 0)
          .with_column('c', lambda x: x.a + 1)
          .with_column_renamed('a', 'A')
          .with_column('d', lambda x: x.A ** 2)
          .select(['A', 'b', 'c'])
          .to_df())
    assert piped_df.equals(other_piped_df), 'Pipe class does not work.'

def test_pipe_with_pandas_method():
    df_dict = fd.apply(lambda x: x.to_dict())(DF)
    assert df_dict == DF.to_dict(), 'Apply function does not apply correctly.'
    df_with_nulls = DF.assign(c=[np.nan, np.nan, 1, 2, 3])
    isnulls = fd.apply(lambda x: x.c.isnull().tolist())(df_with_nulls)
    assert isnulls == [True, True, False, False, False], (
            'Apply function does not apply correctly.')

def test_default_join():
    other_df = pd.DataFrame({'a': [5, 2, 3, 4, 1], 'c': [5, 4, 3, 2, 1]})
    joined_c = fd.join(other_df, ['a'], 'inner')(DF).c.tolist()
    assert joined_c == [1, 4, 3, 2, 5], 'Default join is incorrect.'

def test_map():
    pass

def test_flat_map():
    pass

def test_drop():
    pass

def test_groupby_agg():
    pass

def test_order_by():
    pass
