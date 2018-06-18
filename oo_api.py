# TODO: this is a bit tricky, but some static typing with Pyre might help readability.

import fundas.functional_api as fa

class Pipe(object):
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def to_df(self):
        return self.dataframe

    def __getattribute__(self, name):
        if hasattr(fa, name):
            def fn_to_pipe(*args, **kwargs):
                return Pipe(getattr(fa, name)(*args, **kwargs)(self.dataframe))
            return fn_to_pipe
        else:
            return super().__getattribute__(name)

