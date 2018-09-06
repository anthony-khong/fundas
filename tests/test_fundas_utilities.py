import pandas as pd

import fundas as fd

DF = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b': [1, 2, 3, 2, 1]})

def test_between():
    filtered = fd.filter(lambda x: fd.between(x.b, 2, 3))(DF)
    assert filtered.a.tolist() == [2, 3, 4], 'Between function not correct.'

