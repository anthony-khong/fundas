import numpy as np
import pytest as pt

import pandas as pd
import fundas as fd

DF = pd.DataFrame({
    'a': [1, 2, 3, 4, 5],
    'b': [1, 2, 3, 2, 1]
    })

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
    pass

def test_with_columns_renamed():
    pass

# def test_pipe_function():
    # pipe_results = fd.pipe(
            # df, [
            # fd.select(['a']),
            # fd.filter(lambda x: x.a % 2 == 0),
            # fd.with_column('c', lambda x: x.a + 1),
            # fd.with_column_renamed('a', 'A')
            # ])

# def test_pipe_class():
    # pipe_results = (
        # fd.Pipe(DF)
          # .select(['a'])
          # .filter(lambda x: x.a % 2 == 0)
          # .with_column('c', lambda x: x.a + 1)
          # .with_column_renamed('a', 'A')
          # .consume())
