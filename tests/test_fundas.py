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
    pass

def test_with_columns():
    pass

def test_with_column_renamed():
    pass

def test_with_columns_renamed():
    pass

# def test_pipe():
    # pipe_results = fd.pipe(
            # df, [
            # fd.select(['a']),
            # fd.filter(lambda x: x.a % 2 == 0),
            # fd.with_column('c', lambda x: x.a + 1),
            # fd.with_column_renamed('a', 'A')
            # ])
